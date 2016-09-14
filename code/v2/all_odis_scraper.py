from bs4 import BeautifulSoup
import sys, urllib2

URL = ("http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;page=",";template=results;type=aggregate;view=results")
TOTAL_PAGES = 78

def get_html(page_num):
	url = URL[0] + str(page_num) + URL[1]
	cricfile = urllib2.urlopen(url)
	crichtml = cricfile.read()
	cricfile.close()
	return crichtml

def get_match_urls(page):
	soup = BeautifulSoup(page)
  	siteurl = "http://www.espncricinfo.com"
  	return [siteurl + atag.get('href') for atag in soup.find_all("a", text="Match scorecard")]

def main():
	outfile = open("match_urls.txt", "w")
	for pg in xrange(TOTAL_PAGES):
		html_content = get_html(pg+1)
		if html_content:
			outfile.write("\n".join(get_match_urls(html_content)))
	outfile.write("\n")
	outfile.close()

if __name__ == '__main__':
	main()