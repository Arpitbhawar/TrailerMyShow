import urllib2 as ul
from bs4 import BeautifulSoup
baseurl="http://www.imdb.com"
nameurl = "/find?s=tt&q="
name = str(raw_input("Enter movie name "))
response = ul.urlopen(baseurl+nameurl+name)
page_content = response.read()
soup = BeautifulSoup(page_content)
link = soup.table.a['href']
ratingurl = baseurl+link
response2 = ul.urlopen(ratingurl)
soup2 = BeautifulSoup(response2.read())
print soup2.findAll("div", { "class" : "star-box-details" })[0].span.contents[0]
duration = soup2.findAll("div", { "class" : "infobar" })[0].time.contents[0]
print duration.strip()
genre = soup2.findAll("span", {"itemprop" : "genre"})
for i in genre:
	print i.contents[0]


