#! /usr/bin/python

import httplib2
import os
import requests
import re
import sys

from datetime import datetime
from bs4 import BeautifulSoup
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
HEADERS = {'User-Agent': UA}

HOUSES = [
    {
        'zillow': 'https://www.zillow.com/homes/3003-Monroe-St-Santa-Clara,-CA-95051_rb/19552594_zpid/',
        'redfin': 'https://www.redfin.com/CA/Santa-Clara/3003-Monroe-St-95051/home/1294779',
        'sheet_id': '1BJ7cUThSWkcNYWdzmr9qW9MOHDVD2qWBl79dk7gUSZg',
        'sheet_name': '3003Monroe',
    },
    {
        'zillow': 'https://www.zillow.com/homes/43474-Newport-Dr-Fremont,-CA-94538_rb/25041322_zpid/',
        'redfin': 'https://www.redfin.com/CA/Fremont/43474-Newport-Dr-94538/home/527548',
        'sheet_id': '1VkUrhI5i4CfnvKJmLAiwaYlGaHiOhK_ieQiHQ4hIwtk',
        'sheet_name': 'EstimateHistory',
    },
    {
        'zillow': 'https://www.zillow.com/homes/3321-Pruneridge-Ave-Santa-Clara,-CA-95051_rb/19598205_zpid/',
        'redfin': 'https://www.redfin.com/CA/Santa-Clara/3321-Pruneridge-Ave-95051/home/737513',
        'sheet_id': '1rOrigbqCd68_QdDS-oWWiMWx2PPraIPCTOvPaPsS9nk',
        'sheet_name': 'EstimateHistory',
    },
    {
        'zillow': 'https://www.zillow.com/homes/4596-Bradley-Circle-.num.21-Troy,-MI-48085_rb/2090416087_zpid/',
        'redfin': 'https://www.redfin.com/MI/Troy/4596-Bradley-Cir-48085/unit-21/home/144011152',
        'sheet_id': '1XuDD2O7_-UKZSAguuJjAfSOQtY575UvOQmmWJCeO0DQ',
        'sheet_name': 'EstimateHistory',
    },
    {
        'zillow': 'https://www.zillow.com/homes/116-Canis-St-Georgetown,-TX-78628_rb/331483116_zpid/',
        'redfin': 'https://www.redfin.com/TX/Georgetown/116-Canis-St-78628/home/167600371',
        'sheet_id': '1BJ7cUThSWkcNYWdzmr9qW9MOHDVD2qWBl79dk7gUSZg',
        'sheet_name': '116Canis',
    },
    {
        'zillow': 'https://www.zillow.com/homes/4182-Moncure-Dr-Lilburn,-GA-30047_rb/338361810_zpid/',
        'redfin': 'https://www.redfin.com/GA/Lilburn/4182-Moncure-Dr-30047/unit-30/home/177328740',
        'sheet_id': '1BJ7cUThSWkcNYWdzmr9qW9MOHDVD2qWBl79dk7gUSZg',
        'sheet_name': '4182Moncure',
    },
    {
        'zillow': 'https://www.zillow.com/homes/1217-Palmetto-Dr-Forney,-TX-75126_rb/2062692235_zpid/',
        'redfin': 'https://www.redfin.com/TX/Heath/1217-Palmetto-Dr-75126/home/180051541',
        'sheet_id': '1BJ7cUThSWkcNYWdzmr9qW9MOHDVD2qWBl79dk7gUSZg',
        'sheet_name': '1217Palmetto',
    },
]


# All the sheets code is from https://developers.google.com/sheets/api/quickstart/python
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(
            'client_id.json', 'https://www.googleapis.com/auth/spreadsheets')
        flow.user_agent = 'HouseEstimate'
        credentials = tools.run_flow(flow, store)
    return credentials

def get_zillow_value(node):
  cc = [c for c in node]
  return cc[-1].text

def format_zillow_number(val):
  if 'M' not in val:
    return val
  s = re.search('([0-9\.]+)', val)
  val = int(float(s.groups()[0])*1000000)
  return '$%s' % f"{val:,}"

def get_soup(url):
  r = requests.get(url, headers = HEADERS)
  return BeautifulSoup(r.text, 'html.parser')

def get_zestimate(url):
  soup = get_soup(url)
  nodes = soup.find_all('span', {'data-testid': 'zestimate-text'})
  try:
    estimate = get_zillow_value(nodes[0])
  except:
    estimate = ''
  try:
    rent_estimate = get_zillow_value(nodes[1])
  except:
    rent_estimate = ''
  try:
    erange = soup.find('h5').text
    low, high = map(format_zillow_number, erange.split(' - '))
  except:
    low = ''
    high = ''
  return (estimate, low, high, rent_estimate)

def get_redfin_estimate(url):
  soup = get_soup(url)
  try:
    estimate = soup.find('div', {'class': 'statsValue'}).text
  except:
    try:
      estimate = soup.find('span', {'data-rf-test-id': 'avmLdpPrice'}).find('span', {'class': 'value'}).text
    except:
      estimate = ''
  try:
    rent_estimate = soup.find('p', {'class': 'font-size-medium'}).text.split(' ')[0]
  except:
    rent_estimate = ''
  return (estimate, rent_estimate)

def main():
  for house in HOUSES:
    if 'skip' in house and house['skip']:
        continue
    try:
      estimate = [datetime.now().strftime('%m/%d/%Y')]
      # get redfin estimate
      try:
        estimate.extend(get_redfin_estimate(house['redfin']))
      except:
        estimate.extend(['', ''])
      # get zestimate
      try:
        estimate.extend(get_zestimate(house['zillow']))
      except:
        estimate.extend(['', '', '', ''])
      print(estimate)
      # insert into google sheet
      credentials = get_credentials()
      http = credentials.authorize(httplib2.Http())
      discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                      'version=v4')
      service = discovery.build('sheets', 'v4', http=http,
                                discoveryServiceUrl=discoveryUrl)
      sheetName = house['sheet_name']
      body = {
        'range': sheetName,
        'values': [estimate]
      }
      result = service.spreadsheets().values().append(
          spreadsheetId=house['sheet_id'],
          range=sheetName,
          valueInputOption='USER_ENTERED',
          body=body).execute()
      print(result)
    except:
      pass

if __name__ == "__main__":
  main()
