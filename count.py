#!/usr/bin python
import oauth2
import urlparse
import pytumblr
import json
from unicodedata import normalize
from pprint import pprint

REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
ACCESS_TOKEN_URL  = 'http://www.tumblr.com/oauth/access_token'
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'VMXZOL8hIJ0iaFhjjErPWACD2hAGnWXwaTKskG67ZFuWAz5pfK',
  'knwMMzMlCmTZGvlXHhtfUFs1qm0NxMqsBEdbKtYDYVa3fuNw2U',
  'AjVTT65vgbioccIJ9I89Ee6Ug91UGtLK9REUjAlfvdtKmTtCsL',
  'BCADjechYrTsfZFK154mOohXkMP2kOpE0WW8gDIxlueU3viLzC'
)

followers = []

for offset in range(0,582,20):
    response = client.followers('nasedbab.tumblr.com', offset=offset)['users']
    for i in range(0,20):
        try:
            user = response[i]['name'].encode('ascii', 'ignore') #extract name field and convert from unicode
            followers.append(user)
        except IndexError:
            break
    print "ok"
        

#print followers

fh = open('out', 'w')
for user in followers:
    fh.write(user+"\n")
fh.close()
