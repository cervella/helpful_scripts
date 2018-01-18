from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from urllib.request import urlopen
import re
import csv
from collections import defaultdict



dead_people = []

page = 1

titles = set(("Enterprises", "Manager", "Chief", "Corporal", "Police", "Detective", "Correctional", "Patrol", "Border", "Officer", "Deputy", "Trooper", "Manager", "Senior", "Agent", "Correction", "Sheriff"))

while page <= 5:
	url = 'http://www.nleomf.org/facts/recently-fallen/recently-fallen-2017/index.jsp?page='
	webpage = urlopen(url+str(page))
	only_p_tags = SoupStrainer("p")

	soup = BeautifulSoup(webpage, 'html.parser')

	art = soup.select(".4columns div p p")[0] # this will be the big unclosed p tag starting at the first officer entry

	ps = str(art).split("<p>")

	for p in (p for p in ps if (not re.search('paginat', p)) and len(p.strip())):
		lines = p.split("<br/>")
		imdate, title_name, dep = lines[0:3]
		dep_state = str(dep).split("\xa0")
		title_name = iter(BeautifulSoup(title_name, 'html.parser').text.strip().split(' '))
		title = []
		t = next(title_name)
		while t in titles:
		    title.append(t)
		    t = next(title_name)
		title = " ".join(title)
		name = " ".join([t] + list(title_name))
		og_dict = {"name": name,
		                    "title": title,
		                    "dept": " ".join(dep_state[0:-1]).strip(),
		                    'state': dep_state[-1].strip()}
		new = og_dict.copy()
		dead_people.append(new)
	page += 1

for person in dead_people:
	with open("dead_file.csv", 'w') as result_file:
		fieldnames=['name', 'title', 'dept', 'state']
		#wr = csv.DictWriter(result_file, fieldnames=fieldnames)
		#wr.writeheader()
		wr = csv.writer(result_file)
		wr.writerow(dead_people)




	

