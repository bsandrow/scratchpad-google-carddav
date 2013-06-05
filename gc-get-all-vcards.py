#!/usr/bin/env python

import os
from collections     import namedtuple
from pprint          import pprint as PP
from xml.dom.minidom import parseString as parse_xml

import requests

VCardURL = namedtuple('VCardURL', 'name url')

username = os.environ.get('GUSER', None)
password = os.environ.get('GPASS', None)

base_url = "https://google.com"
top_url  = "%s/m8/carddav/principals/__uids__/%s/lists/default/" % (base_url, username)

response = requests.request('PROPFIND', top_url, auth=(username, password))

if response.status_code != 207:
    print "ERROR: Could not fetch list of vcards."
    print "HEADERS: ",
    PP(response.headers)

dom = parse_xml(response.text)
response_elements = dom.getElementsByTagName('d:response')

def is_card_entry(el):
    ct = el.getElementsByTagName('d:getcontenttype')
    return len(ct) > 0 and ct[0].hasChildNodes() and ct[0].childNodes[0].data == 'text/vcard'

vcards = [
    VCardURL(name, "%s%s" % (top_url, name))
        for name in [
            el.getElementsByTagName('d:displayname')[0].childNodes[0].data
            for el in filter(is_card_entry, response_elements)
        ]
]

for vcard in vcards:
    print "Fetching vcard %s..." % vcard.name
    response = requests.get(vcard.url, auth=(username, password))
    filename = "%s.vcf" % vcard.name

    if response.status_code not in ('200', 200):
        print "Error: Got HTTP Status Code: %s" % response.status_code
        print "== RESPONSE HEADERS DUMP =="
        for item in response.headers.items():
            print "%s: %s" % item

    with open(filename, 'wb+') as fh:
        fh.write(response.content)
