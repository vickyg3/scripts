#! /usr/bin/python

import requests
import xmltodict

if __name__ == "__main__":
  zws_id = 'X1-ZWz196sfugrtaj_6a5jo'
  zpid = '19552594'
  zillow_url = 'http://www.zillow.com/webservice/GetZestimate.htm?rentzestimate=true&zws-id=%(zws_id)s&zpid=%(zpid)s' % locals()
  user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
  headers = {'User-Agent': user_agent}
  try:
    xml = xmltodict.parse(requests.get(zillow_url).text)
    zestimate = xml['Zestimate:zestimate']['response']['zestimate']
    value = float(zestimate['amount']['#text'])/1000000
    print '%(value)0.3fM' % locals()
  except:
    print 'N/A'
