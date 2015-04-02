# usage: 
# python scraper.py

# imports
from bs4 import BeautifulSoup
import urllib2

# parameters
outcsv = "out.csv"

# get the html content of the given page no.
def getPage(pageno):
  url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;page=" + str(pageno) + ";template=results;type=batting;view=innings;wrappertype=print"
  try:  
    cricfile = urllib2.urlopen(url)
    crichtml = cricfile.read()
    cricfile.close()
    return crichtml
  except:
    return None

# parse the table and write to a file
def parsetable(html, tableno, outfile):
  soup = BeautifulSoup(html)
  table = soup.findAll('table', attrs={'class':'engineTable'})[tableno]
  table_rows = table.find('tbody').findAll('tr')
  for row in table_rows:
    cols = [element.text.strip().encode('utf8') for element in row.findAll('td')]
    csvrow = ','.join(cols)
    outfile.write(csvrow + '\n')

# main
outfile = open(outcsv,'w')
pageno = 1
while True:
  crichtml = getPage(pageno)
  if crichtml:
    print "Reading page: " + str(pageno)
    parsetable(crichtml, 2, outfile)
    pageno += 1
  else:
    print "Finished reading (" + str(pageno) + " pages)"
    break;
outfile.close()
