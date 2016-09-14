from bs4 import BeautifulSoup
import urllib2, json

def get_page(url):
  try:  
    cricfile = urllib2.urlopen(url)
    crichtml = cricfile.read()
    cricfile.close()
    return crichtml
  except:
    return None

def extract_bat_rows(rows_list):
	innings = []
	for row in rows_list:
		innings.append([tag.get_text().encode('ascii','ignore').strip() for tag in row.find_all('td')][1:])
	return innings

def extract_bowl_rows(rows_list):
	innings = []
	for row in rows_list:
		innings.append([tag.get_text().encode('ascii','ignore').strip() for tag in row.find_all('td')][1:-2])
	return innings

def find_team_batting_order(match_soup):
	batting_order = []
	batting_tables = match_soup.find_all('table', attrs={'class':'batting-table innings'})
	for table in batting_tables:
		batting_order.append(table.find('tr', attrs={'class':'tr-heading'}).find('th', attrs={'class':'th-innings-heading'}).get_text().encode('ascii','ignore').strip())
	return batting_order

def extract_from_url(url):
	print "Extracting match: " + url
	print_url = url + '?view=scorecard;wrappertype=print'

	match_soup = BeautifulSoup(get_page(url), "html.parser")
	print_match_soup = BeautifulSoup(get_page(print_url), "html.parser")

	bat_rows1 = print_match_soup.find('table', attrs={'id':'inningsBat1'}).find_all('tr', attrs={'class':'inningsRow'})
	bat_rows2 = print_match_soup.find('table', attrs={'id':'inningsBat2'}).find_all('tr', attrs={'class':'inningsRow'})

	bat_innings1 = extract_bat_rows(bat_rows1)
	bat_innings2 = extract_bat_rows(bat_rows2)

	bowl_rows1 = print_match_soup.find('table', attrs={'id':'inningsBowl1'}).find_all('tr', attrs={'class':'inningsRow'})
	bowl_rows2 = print_match_soup.find('table', attrs={'id':'inningsBowl2'}).find_all('tr', attrs={'class':'inningsRow'})

	bowl_innings1 = extract_bowl_rows(bowl_rows1)
	bowl_innings2 = extract_bowl_rows(bowl_rows2)

	fow1 = [span.get_text().encode('ascii','ignore').strip() for span in match_soup.find_all('a', attrs={'class':'fowLink'})[0].find_all('span')]
	fow2 = [span.get_text().encode('ascii','ignore').strip() for span in match_soup.find_all('a', attrs={'class':'fowLink'})[1].find_all('span')]

	venue = match_soup.find_all('div', attrs={'class':'space-top-bottom-5'})[2].find('a').get_text().encode('ascii','ignore').strip()
	result = match_soup.find('div', attrs={'class':'innings-requirement'}).get_text().encode('ascii','ignore').strip()

	batting_order = find_team_batting_order(match_soup)
	match_notes = [row.get_text().encode('ascii','ignore').strip() for row in print_match_soup.find_all('table', attrs={'class':'notesTable'})[0].find_all('tr',attrs={'class':'notesRow'})]

	match = {}
	match['url'] = url
	match['venue'] = venue
	match['result'] = result
	match['batting_order'] = batting_order
	match['other_notes'] = match_notes
	match['batting_innings'] = [bat_innings1, bat_innings2]
	match['bowling_innings'] = [bowl_innings1, bowl_innings2]
	match['fow'] = [fow1,fow2]

	filename = url.split('/')[-1].split('.')[0] + ".json"
	with open(filename, 'w') as outfile:
		json.dump(match, outfile)

urls = ['http://www.espncricinfo.com/ci/engine/match/64154.html','http://www.espncricinfo.com/ci/engine/match/65294.html', 'http://www.espncricinfo.com/ci/engine/match/65184.html']
for url in urls:
	extract_from_url(url)