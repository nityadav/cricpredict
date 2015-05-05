from bs4 import BeautifulSoup
from collections import Counter
import urllib2, re

# parameters
start_date = "13+Mar+2007"
end_date = "29+Mar+2015"
playing_teams = ["Australia","India"]
playing_teams.sort()

# data
Team_Number = {"Australia":"2", "Bangladesh":"3", "England":"4", "India":"6", "New Zealand":"7", "Pakistan":"8", "South Africa":"9", "Sri Lanka":"10", "West Indies":"11", "Zimbabve":"12"}

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
  return [row.find_all('td', attrs={'class':''})[-1].get_text() for row in rows][:-1]

def get_partnerships(match_soup, innings):
  total = int(match_soup.find_all('tr',attrs={'class':'total-wrap'})[inning_num-1].find('td',attrs={'class':'bold'}).get_text())
  fow = match_soup.find_all('a', attrs={'class':'fowLink'})[innings-1]
  fow_vals = [0]
  fow_vals += [int(span.get_text().split()[0].split('-')[1]) for span in fow.find_all('span')]
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

# convert the information into features
def feature_highest_opening(match_soup, reverse):
  first_innings = get_partnerships(match_soup,1)[0]
  second_innings = get_partnerships(match_soup,2)[1]
  true_val = first_innings < second_innings
  if reverse:
    return not true_val
  else:
    return true_val

def feature_more_than_3_wkts(match_soup, reverse):
  first_innings = get_max_wickets(match_soup,1) > 3
  second_innings = get_max_wickets(match_soup,2) > 3
  if reverse:
    
  else:


# main starts here
page_no = 1
num_matches = 0
while True:
  result_url = get_search_results_url(page_no)
  page = get_page(result_url)
  match_urls = gather_match_urls(page)
  if match_urls:
    for match_url in match_urls:
      reverse = False
      match_soup = BeautifulSoup(get_page(match_url))
      winner = who_won(match_soup)
      if winner not in playing_teams: # means no result
        continue
      batting_order = find_team_batting_order(match_soup)
      if batting_order[0] != playing_teams[0]:
        reverse = True
      feature_highest_opening(match_soup, reverse)
      num_matches += 1
      page_no += 1
  else: # denotes the last page
    break

print "Total matches found: " + str(num_matches)
# main ends here