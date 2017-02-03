#! /usr/bin/python

import pyperclip
import requests
import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
  print "Usage: %s <redfin url>" % sys.argv[0]
  sys.exit(1)

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
try:
  data = requests.get(sys.argv[1], headers = headers).text
  #f = open("/tmp/data.txt", "w")
  #f.write(data.encode('utf-8'))
  #f.close()
  #data = open("/tmp/data.txt").read()
  soup = BeautifulSoup(data, "html.parser")
  address = soup.find('span', {'data-rf-test-id':'abp-streetLine'}).text + str(soup.find('span', {'data-rf-test-id':'abp-cityStateZip'}).text)
  price = soup.find('div', {'data-rf-test-id':'abp-price'}).find('div').text.replace("$","").replace(",","")
  estimate = soup.find('span', {'data-rf-test-id':'avmLdpPrice'}).find('span', {'class': 'value'}).text.replace("$","").replace(",","")
  sqft = soup.find('div', {'data-rf-test-id':'abp-sqFt'}).find('span').find('span').text.replace(",","")
  beds = soup.find('div', {'data-rf-test-id':'abp-beds'}).find('div').text
  baths = soup.find('div', {'data-rf-test-id':'abp-baths'}).find('div').text
  schools = "\t".join([row.find('div', {'class': 'rating'}).text for row in soup.find('div', {'class': 'schools-content'}).findAll('tr')[1:]])
  url = sys.argv[1]
  print "Address,Price,Estimate,Sqft,Bed,Bath,Cisco (miles),Google (miles),Schools"
  wret = "=hyperlink(\"%(url)s\",\"%(address)s\")\t%(price)s\t%(estimate)s\t%(sqft)s\t%(beds)s\t%(baths)s\t0\t0\t%(schools)s" % locals()
  print wret
  pyperclip.copy(wret)
except:
  print "Error :("
  raise
else:
  print "Done - copied to clipboard :)"