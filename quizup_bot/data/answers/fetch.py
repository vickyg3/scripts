#! /usr/bin/python

from BeautifulSoup import BeautifulSoup

import csv
import re
import string

pattern = re.compile('[\W_]+')
w = csv.writer(open('general_knowledge.csv', 'wb'))
soup = BeautifulSoup(open('index.html'))
for row in soup.find('table').findAll('tr')[1:]:
	q, a =  row.findAll('td')[0].string, row.findAll('td')[1].string
	if not q:
		continue
	q = pattern.sub('', q)
	w.writerow((q.lower(),a.lower()))