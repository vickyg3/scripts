#! /usr/bin/python

import httplib2
import os
import requests
import sys
import xmltodict

from datetime import datetime
from bs4 import BeautifulSoup
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

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

def get_zestimate(data, rent):
  key = 'rentzestimate' if rent else 'zestimate'
  zestimate = data['Zestimate:zestimate']['response'][key]
  value = '$' + zestimate['amount']['#text']
  low = '$' + zestimate['valuationRange']['low']['#text']
  high = '$' + zestimate['valuationRange']['high']['#text']
  return (value, low, high)

if __name__ == "__main__":
  redfin_urls = [
      'https://www.redfin.com/CA/Santa-Clara/3003-Monroe-St-95051/home/1294779',
      'https://www.redfin.com/CA/Fremont/43474-Newport-Dr-94538/home/527548',
      'https://www.redfin.com/CA/Santa-Clara/3321-Pruneridge-Ave-95051/home/737513',
      'https://www.redfin.com/MI/Troy/4621-Bradley-Cir-48085/home/113431822']
  zws_id = 'X1-ZWz196sfugrtaj_6a5jo'
  zpids = ['19552594', '25041322', '19598205', '2087627195']
  user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
  headers = {'User-Agent': user_agent}
  spreadsheetIds = [
      '1BJ7cUThSWkcNYWdzmr9qW9MOHDVD2qWBl79dk7gUSZg',
      '1VkUrhI5i4CfnvKJmLAiwaYlGaHiOhK_ieQiHQ4hIwtk',
      '1rOrigbqCd68_QdDS-oWWiMWx2PPraIPCTOvPaPsS9nk',
      '1XuDD2O7_-UKZSAguuJjAfSOQtY575UvOQmmWJCeO0DQ']
  for i in range(len(redfin_urls)):
    redfin_url = redfin_urls[i]
    zpid = zpids[i]
    zillow_url = 'http://www.zillow.com/webservice/GetZestimate.htm?rentzestimate=true&zws-id=%(zws_id)s&zpid=%(zpid)s' % locals()
    try:
      estimate = [datetime.now().strftime('%m/%d/%Y')]
      # get redfin estimate
      try:
        soup = BeautifulSoup(requests.get(redfin_url, headers=headers).text, 'html.parser')
        try:
          redfin_estimate = soup.find('div', {'data-rf-test-id': 'avm-price'}).find('div').text
        except:
          try:
            redfin_estimate = soup.find('span', {'data-rf-test-id': 'avmLdpPrice'}).find('span', {'class': 'value'}).text
          except:
            redfin_estimate = ''
        estimate.append(redfin_estimate)
      except:
        estimate.append('')
      # get zestimate
      try:
        xml = xmltodict.parse(requests.get(zillow_url).text)
        estimate.extend(get_zestimate(xml, False))
      except:
        estimate.extend(['', '', ''])
      try:
        estimate.extend(get_zestimate(xml, True))
      except:
        estimate.extend(['', '', ''])
      # insert into google sheet
      credentials = get_credentials()
      http = credentials.authorize(httplib2.Http())
      discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                      'version=v4')
      service = discovery.build('sheets', 'v4', http=http,
                                discoveryServiceUrl=discoveryUrl)
      sheetName = 'EstimateHistory'
      body = {
        'range': sheetName,
        'values': [estimate]
      }
      result = service.spreadsheets().values().append(
          spreadsheetId=spreadsheetIds[i],
          range=sheetName,
          valueInputOption='USER_ENTERED',
          body=body).execute()
      print result
    except:
      raise
      pass
