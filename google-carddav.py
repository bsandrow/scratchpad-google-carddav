#!/usr/bin/env python

from xml.dom.minidom import parseString as parse_xml
import requests

base = "https://google.com"

# Note: The second %s can be replaced by $GUSER, but there's no point because
#       'default' references the currently authenticated user. It could be
#       possible to use this to access someone else's addressbook, provided the
#       permissions are setup to allow you access.
url  = "%s/m8/carddav/principals/__uids__/%s/lists/default/" % (base, 'default')

def get_all_contact_vcards(username, password):
    response = requests.request('PROPFIND', top_url, auth=(username, password))

    if response.status_code != 207:
        print "ERROR: Could not fetch list of address book entries."
        print "== Response Headers Dump =="
        for item in response.headers.items():
            print "%s: %s" % item

    dom = parse_xml(response.content)

    VCardURL = namedtuple('VCardURL', 'name url')
    def is_vcard(el):
        ct = el.getElementsByTagName('d:getcontenttype')
        # d:getcontenttype exists, and has a text node containing 'text/vcard'
        return len(ct) > 0 and ct[0].hasChildNodes() and ct[0].childNodes[0].data == 'text/vcard'

    vcards = []
    for node in filter(is_vcard, dom.getElementsByTagName('d:response')):
        name = el.getElementsByTagName('d:displayname')[0].childNodes[0].data
        vcards.append( VCardURL(name, "%s%s" % (top_url, name))

    vcard_dict = dict()
    for vcard in vcards:
        response = requests.get(vcard.url, auth=(username, password))
        if response.status_code != 200:
            print "Error: Got 'HTTP Status Code %s' response fetching URL: %s" % (response.status_code, vcard.url)
            print "== HEADER DUMP =="
            for item in response.headers.items():
                print "%s: %s" % item

        vcard_dict[vcard.name] = response.text

    return vcard_dict

if __name__ == '__main__':
    import argparse
    import os
    import sys

    try:    username = os.environ['GUSER']
    except: sys.exit("Error: Environment variable $GUSER is not set.")

    try:    password = os.environ['GPASS']
    except: sys.exit("Error: Environment variable $GPASS is not set.")

    parser = argparse.ArgumentParser(description="Let's run some CardDAV queries, shall we?")
    parser.add_argument('action', help='The action to take')
    options = parser.parse_args()

    
