#! /usr/bin/python

import urllib
import urllib2
import json

class Dapp(object):
    url = "http://open.dapper.net/transform.php?dappName=%s&transformer=JSON&applyToUrl=%s"
    def _geturl(dapp_name, apply_to_url, params):
        return url % (dapp_name, urllib.quote(apply_to_url))

    def get_data(dapp_name, apply_to_url, params):
        return json.load(urllib2.urlopen(_geturl(dapp_name, apply_to_url, params)))
