from bs4 import BeautifulSoup
from collections import Counter
import urllib2, re, random

# parameters
start_date = "13+Mar+2007"
end_date = "29+Mar+2015"
playing_teams = ["England","India"]
playing_teams.sort()

# data
Team_Number = {"England":"1", "Australia":"2", "South":"3", "West":"4", "New":"5", "India":"6", "Pakistan":"7", "Sri":"8"}

# extract integer number
def extract_int(int_str):
  return int(re.search(r'\d+', int_str).group())

# form url to see the results based on the input parameters
def get_search_results_url(page_no):
  team1 = Team_Number[playing_teams[0]]
  team2 = Team_Number[playing_teams[1]]
  return "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;opposition=" + team2 + ";page=" + str(page_no) + ";spanmax1=" + end_date + ";spanmin1=" + start_date + ";spanval1=span;team=" + team1 + ";template=results;type=team;view=results"

# get the html content for the given url
def get_page(url):
  try:  
    cricfile = urllib2.urlopen(url)
    crichtml = cricfile.read()
    cricfile.close()
    return crichtml
  except:
    return None

def gather_match_urls(page):
  soup = BeautifulSoup(page)
  siteurl = "http://www.espncricinfo.com"
  return [siteurl + atag.get('href') for atag in soup.find_all("a", text="Match scorecard")]

def who_won(match_soup):
  return match_soup.find('div', attrs={'class':'innings-requirement'}).get_text().split()[0]

def find_team_batting_order(match_soup):
  batting_order = []
  batting_tables = match_soup.find_all('table', attrs={'class':'batting-table innings'})
  for table in batting_tables:
    batting_order.append(table.find('tr', attrs={'class':'tr-heading'}).find('th', attrs={'class':'th-innings-heading'}).get_text().split()[0])
  return batting_order

def get_batting_scores(match_soup, innings):
  table = match_soup.find_all('table', attrs={'class':'batting-table innings'})[innings-1]
  rows = table.find_all('tr', class_=lambda x: x not in ['dismissal-detail','tr-heading','extra-wrap'])
  return [int(row.find('td', attrs={'class':'bold'}).get_text()) for row in rows][:-1]

def get_strike_rates(match_soup, innings):
  table = match_soup.find_all('table', attrs={'class':'batting-table innings'})[innings-1]
  rows = table.find_all('tr', class_=lambda x: x not in ['dismissal-detail','tr-heading','extra-wrap'])
  strike_rates = []
  for row in rows[:-1]:
    str_val = row.find_all('td', attrs={'class':''})[-1].get_text()
    try:
      strike_rates.append(float(str_val))
    except ValueError:
      strike_rates.append(0.00)
  return strike_rates

def get_total(match_soup, innings):
  return int(match_soup.find_all('tr',attrs={'class':'total-wrap'})[innings-1].find('td',attrs={'class':'bold'}).get_text())

def get_partnerships(match_soup, innings):
  total = get_total(match_soup,innings)
  fow = match_soup.find_all('a', attrs={'class':'fowLink'})[innings-1]
  fow_vals = [0]
  fow_vals += [extract_int(span.get_text().split()[0].split('-')[1]) for span in fow.find_all('span')]
  fow_vals.append(total)
  return [fow_vals[i]-fow_vals[i-1] for i in range(1,len(fow_vals))]

def get_max_wickets(match_soup, innings):
  table = match_soup.find_all('table', attrs={'class':'batting-table innings'})[innings-1]
  rows = table.find_all('tr', class_=lambda x: x not in ['dismissal-detail','tr-heading','extra-wrap'])
  dismissal = []
  for row in rows:
    dismiss_info = row.find('td', attrs={'class':'dismissal-info'})
    if dismiss_info:
      parts = dismiss_info.get_text().split('b ')
      if len(parts) == 2:
        dismissal.append(parts[1].strip())
  return Counter(dismissal).most_common(1)[0][1]

######################################
# convert the information into features and labels
def feature_highest_opening(match_soup, reverse):
  first_innings = get_partnerships(match_soup,1)[0]
  second_innings = get_partnerships(match_soup,2)[1]
  true_val = first_innings < second_innings
  if reverse:
    return int(not true_val)
  else:
    return int(true_val)

def feature_3_wkts(match_soup, reverse):
  first_innings = int(get_max_wickets(match_soup,1) > 3)
  second_innings = int(get_max_wickets(match_soup,2) > 3)
  if reverse:
    return 2*first_innings + second_innings
  else:
    return 2*second_innings + first_innings

def feature_century(match_soup, reverse):
  first_innings = int(max(get_batting_scores(match_soup,1)) >= 100)
  second_innings = int(max(get_batting_scores(match_soup,2)) >= 100)
  if reverse:
    return 2*first_innings + second_innings
  else:
    return 2*second_innings + first_innings

def feature_fast_batting(match_soup, reverse):
  first_innings_strs = get_strike_rates(match_soup,1)
  first_innings_runs = get_batting_scores(match_soup,1)
  first_innings = len([score for i,score in enumerate(first_innings_runs) if (score >= 50 and first_innings_strs[i] >= 100)]) >= 1
  second_innings_strs = get_strike_rates(match_soup,2)
  second_innings_runs = get_batting_scores(match_soup,2)
  second_innings = len([score for i,score in enumerate(second_innings_runs) if (score >= 50 and second_innings_strs[i] >= 100)]) >= 1
  if reverse:
    return 2*first_innings + second_innings
  else:
    return 2*second_innings + first_innings

def feature_total_score(match_soup, reverse):
  first_innings = get_total(match_soup,1) >= 300
  second_innings = get_total(match_soup,2) >= 300
  if reverse:
    return 2*first_innings + second_innings
  else:
    return 2*second_innings + first_innings

def feature_100_partnership(match_soup, reverse):
  first_innings = max(get_partnerships(match_soup,1)) >= 100
  second_innings = max(get_partnerships(match_soup,2)) >= 100
  if reverse:
    return 2*first_innings + second_innings
  else:
    return 2*second_innings + first_innings

def feature_two_150(match_soup, reverse2):
  first_innings = sum(sorted(get_batting_scores(match_soup,1))[0:2]) >= 120
  second_innings = sum(sorted(get_batting_scores(match_soup,2))[0:2]) >= 120
  if reverse:
    return 2*first_innings + second_innings
  else:
    return 2*second_innings + first_innings

##################
# main starts here
page_no = 1
num_matches = 0
train_file = open("data/" + "_".join(playing_teams) + "_train.csv",'w')
test_file = open("data/" + "_".join(playing_teams) + "_test.csv",'w')
test_matches_file = open("data/" + "_".join(playing_teams) + "_test_matches.csv",'w')
feature_functions = [feature_highest_opening, feature_3_wkts, feature_century, feature_fast_batting, feature_total_score, feature_100_partnership, feature_two_150]
samples = []
samples_matches = []
while True:
  result_url = get_search_results_url(page_no)
  page = get_page(result_url)
  match_urls = gather_match_urls(page)
  if match_urls:
    for match_url in match_urls:
      print "Scraping match: " + match_url
      samples_matches.append(match_url)
      reverse = False
      match_soup = BeautifulSoup(get_page(match_url))
      winner = who_won(match_soup)
      if winner not in playing_teams: # means no result
        continue
      batting_order = find_team_batting_order(match_soup)
      if batting_order[0] != playing_teams[0]:
        reverse = True
      # start creating labels and features
      label = str(playing_teams.index(winner)*2 - 1)
      feature_line = ",".join([label] + [str(feature_func(match_soup,reverse)) for feature_func in feature_functions])
      samples.append(feature_line)
      num_matches += 1
    page_no += 1
  else: # denotes the last page
    break

# break the samples randomly into test and training set
test_indices = random.sample(range(num_matches), num_matches/3)
test_sample = []
test_sample_matches = []
train_sample = []
for i in range(num_matches):
  if i in test_indices:
    test_sample.append(samples[i])
    test_sample_matches.append(samples_matches[i])
  else:
    train_sample.append(samples[i])

train_file.write('\n'.join(train_sample) + '\n')
test_file.write('\n'.join(test_sample) + '\n')
test_matches_file.write('\n'.join(test_sample_matches) + '\n')
train_file.close()
test_file.close()
test_matches_file.close()
print "Total matches found: " + str(num_matches)
# main ends here