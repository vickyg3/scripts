#! /usr/bin/python

import requests
import sys
import re

from bs4 import BeautifulSoup

if __name__ == "__main__":
  redfin_url = 'https://www.redfin.com/CA/Santa-Clara/3003-Monroe-St-95051/home/1294779'
  user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
  headers = {'User-Agent': user_agent}
  try:
    soup = BeautifulSoup(requests.get(redfin_url, headers=headers).text, 'html.parser')
    redfin_estimate = soup.find('div', {'data-rf-test-id': 'avm-price'}).find('div').text
    estimate = re.match("\$([0-9]+),([0-9]+),.*", redfin_estimate).groups()
    print "%s.%sM" % (estimate[0], estimate[1])
  except:
    print 'N/A'
