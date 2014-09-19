#! /usr/bin/python

# Scraper that goes through all services and gets the exchange rates.
# This is cron'ed every hour.

import json
import re
import requests
import sys
from BeautifulSoup import BeautifulSoup

# begin parsers

def xoom_parser(data):
	soup = BeautifulSoup(data)
	return float(re.match(r'^1 USD = (.*) INR$', soup.find('em', {'class': 'fx-rate'}).string).groups()[0])

def m2i_parser(data):
	soup = BeautifulSoup(data)
	return float(re.match('.*USA = ([^ ]+) INR.*', ' '.join(soup.find('marquee').findAll(text = True)).replace('\n', ' ')).groups()[0])

def r2i_parser(data):
	soup = BeautifulSoup(data)
	return float(soup.find('span', {'class': 'exRate'}).string)

def wu_parser(data):
	return float(json.loads(data)['update']['conversion']['targetCurrency']['exchange'])

def rl_parser(data):
	soup = BeautifulSoup(data)
	return float(re.match(r'INR ([0-9\.]+).*', soup.find('span', {'class': 'yellowHighlight'}).string).groups()[0])
	#return float(re.match(r'1 USD = ([0-9\.]+).*', soup.find('span', {'class': 'yellowHighlight'}).string).groups()[0])

def tf_parser(data):
	soup = BeautifulSoup(data)
	return float(soup.find('span', id='lblExchangeRate').string)

def axis_parser(data):
	soup = BeautifulSoup(data)
	return float(re.match(r'USD 1 = Rs\. ([0-9\.]+).*', soup.find('span', id='lblCurrency').string).groups()[0])

def ifr_parser(data):
	soup = BeautifulSoup(data)
	return float(re.match(r'.*1 USD = ([^ ]+).*', ' '.join(soup.find('div', {'class': 'body'}).findAll(text = True)).replace('\n', ' ')).groups()[0])

def sbi_parser(data):
	soup = BeautifulSoup(data)
	return float(soup.findAll('td', {'class': 'content'})[1].string.strip().split(' ')[0])

def ib_parser(data):
	soup = BeautifulSoup(data)
	return float(soup.find('tr', {'bgcolor': '#FFFFFF'}).findAll('td', {'align': 'center'})[1].string)

def royal_parser(data):
	soup = BeautifulSoup(data)
	return float(soup.find('span', id = 'txtbankrate').string)

# end parsers

parsers =  [
				{
					'name': 'Xoom',
					'url': 'https://www.xoom.com/india',
					'parser': xoom_parser,
					'locked_in': True
				},
				{
					'name': 'ICICI Money2India',
					'url': 'http://www.icicibank.com/nri-banking/money_transfer/exchange-rate/iframe_exchange_rate.html',
					'parser': m2i_parser,
					'locked_in': True
				},
				{
					'name': 'Remit2India',
					'url': 'https://www.remit2india.com/sendmoneytoindia/UnitedStates/index.jsp',
					'parser': r2i_parser,
					'locked_in': False
				},
				{
					'name': 'Western Union Money Transfer',
					'url': 'https://www.westernunion.com/ajaxHandler/service/getDelvryOptAndCurrency/?originAmount=0.0&originCountry=US&targetCountry=IN&originCurrency=USD&senderZipCode=&_=1390937227258',
					'parser': wu_parser,
					'locked_in': False
				},
				{
					'name': 'Remit Lite',
					'url': 'https://www.remitlite.com/remitlite/index.jsp',
					'parser': rl_parser,
					'locked_in': False
				},
				{
					'name': 'Transfast',
					'url': 'https://www.transfast.com/sendmoney_IND.aspx',
					'parser': tf_parser,
					'locked_in': True
				},
				{
					'name': 'Axis Remit',
					'url': 'https://www.axisbank.com/WebForms/axis_remit_US/Send-Money-To-India-From-US.aspx',
					'parser': axis_parser,
					'locked_in': False
				},
				{
					'name': 'Indus Fast Remit',
					'url': 'https://www.indusfastremit.com/mobile/exchangeRate.do',
					'parser': ifr_parser,
					'locked_in': True
				},
				{
					'name': 'SBI Remittance',
					'url': 'https://www.statebank.com/RemittanceServiceIndMaster.asp',
					'parser': sbi_parser,
					'locked_in': False
				},
				{
					'name': 'Indian Bank IND Remit',
					'url': 'http://www.timesofmoney.com/remittance/jsp/remitExchangeRate.jsp?partnerId=INB&uiId=INB',
					'parser': ib_parser,
					'locked_in': False
				},
				{
					'name': 'Royal Exchange USA',
					'url': 'https://www.rupees2india.us:462/MoneyTransferUS/LoginPageBankNew.aspx',
					'parser': royal_parser,
					'locked_in': True
				},
			]

def main():
	amount = None
	if len(sys.argv) > 0:
		try:
			amount = int(sys.argv[1])
		except:
			pass
	headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36' }
	for parser in parsers:
		try:
			rate = parser['parser'](requests.get(parser['url'], verify = False, headers = headers).text)
			print parser['name'], "-", rate,
			if amount:
				print "-", (float(rate) * amount)
			else:
				print ""
		except:
			pass

if __name__ == "__main__":
	main()
