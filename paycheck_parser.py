#! /usr/bin/python

from BeautifulSoup import BeautifulSoup

import json
import sys

year_total = {}
soup = BeautifulSoup(open('/Users/vigneshv/Desktop/Print Preview.html', 'r'))
pay_tables = soup.findAll('table', {"id": "ctl00_Content_usgEarnings"})
for table in pay_tables:
    rows = table.findAll('tr')
    cells = rows[0].findAll('th')
    # determine the index of current
    current_index = -1
    for cell_index in range(len(cells)):
        if "current" in ''.join(cells[cell_index].findAll(text = True)).strip().lower():
            current_index = cell_index
            break
    for row in rows[1:]:
        subtract = False
        cells = row.findAll('td')
        label = ''.join(cells[0].findAll(text = True)).strip()
        current = ''.join(cells[current_index].findAll(text = True)).strip().lstrip("$")
        if not current.strip():
            continue
        # handle refunds of the form "($xx.yy)"
        if current[0] == "(" and current[-1] == ")":
            current = current.lstrip("($").rstrip(")")
            subtract = True
        if label not in year_total:
            year_total[label] = 0.0
        if subtract:
            year_total[label] -= float(current.replace(',', ''))
        else:
            year_total[label] += float(current.replace(',', ''))

print json.dumps(year_total, sort_keys=True, indent=4, separators=(',', ': '))
print "done :)"
