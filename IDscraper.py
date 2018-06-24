"""writing a scraper to pull data from the ID SOS website"""

import mechanicalsoup
import ssl
import csv
import re
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import urllib.request
import pandas as pd

browser = mechanicalsoup.StatefulBrowser()
input_as_cand_last_name = 'Jordan'#input("what is the candidate's last name? ")
input_as_cand_first_name = 'Paulette'#input("what is the candidate's first name? ")

form_url = 'https://sos.idaho.gov/ElectionOnlineSearch/SearchCandidate.aspx'

browser.open(form_url)
#browser.follow_link("cand")
form = browser.select_form('#CandSearchForm')
form.set("as_cand_last_name", input_as_cand_last_name)
form.set("as_cand_first_name", input_as_cand_first_name)
form.choose_submit('contrib_button')

response = browser.submit_selected()
soup = BeautifulSoup(response.text, 'html.parser')

dataz = []
head = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
#headers = rows.find_all('th')

#for h in rows:
	#header = h.find_all('th')
	#header = [ele.text.strip() for ele in header]
	#head.append([ele for ele in header if ele])



for row in rows:
	cols = row.find_all('td')
	cols = [ele.text.strip() for ele in cols]
	dataz.append(cols)

df = pd.DataFrame(dataz)
df.to_csv('id_output.csv')