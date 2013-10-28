#! /usr/bin/python

import json
import re
import urllib2

dapp_url = "http://open.dapper.net/transform.php?dappName=arsenal_tv_schedule&transformer=JSON&applyToUrl=http%3A%2F%2Fwww.arsenal.com%2Fusa%2Fnews%2Ffeatures%2Fwhere-to-watch-arsenal"
# Sample string: "October 26 - 7:45am: @ Crystal Palace (Premier League) - NBCSN"
schedule_exp = re.compile(r'^([A-Za-z]+ [0-9]+)[^0-9]*([0-9:amp]+): (.*?) ([^\(]+)\(([^\)]+)\) - (.*)$')
output = []
try:
	data = json.load(urllib2.urlopen(dapp_url))['fields']['matches']
	for datum in data:
		output.append(schedule_exp.match(datum['value']).groups())
	print json.dumps(output)
except:
	print "{}"