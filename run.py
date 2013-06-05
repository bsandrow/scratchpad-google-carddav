#!/usr/bin/env python

from xml.dom.minidom import parseString as parse_xml
import os
import requests

username = os.environ.get('GUSER', None)
password = os.environ.get('GPASS', None)

url = "https://google.com/m8/carddav/principals/__uids__/%s/lists/default/" % username
data = """
<?xml version="1.0" encoding="utf-8" ?>
<card:addressbook-query xmlns:D="DAV:"
                  xmlns:card="urn:ietf:params:xml:ns:carddav">
  <D:prop>
    <D:getetag/>
    <card:address-data>
      <card:prop name="UID"/>
    </card:address-data>
  </D:prop>
  <card:filter test="anyof">
    <card:prop-filter name="EMAIL">
      <card:text-match collation="i;unicode-casemap" match-type="contains">april</card:text-match>
    </card:prop-filter>
  </card:filter>
</card:addressbook-query>
"""
response = requests.request('PROPFIND', url, auth=(username, password))

print "Status Code: %s" % (response.status_code)

print "\n== HEADERS =="
for item in response.headers.items():
    print "%s: %s" % item

print "\n== BODY =="
print parse_xml(response.content).toprettyxml()
