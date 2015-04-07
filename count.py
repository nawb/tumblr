#!/usr/bin python
import sys
import oauth2
import urlparse
import pytumblr
import json
import time
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

sys.stdout.write("Retrieving followers")

followers = []
counter = 0
offset = 0
doneCounting = False
start_time = time.time()

while True:
    response = client.followers('nasedbab.tumblr.com', offset=offset)['users']
    offset = offset + 20
    sys.stdout.flush() #to clear output buffer
    sys.stdout.write(".")

    for i in range(0,20):
        try:
            #extract name field and convert from unicode
            user = response[i]['name'].encode('ascii', 'ignore')
            followers.append(user)
            counter = counter + 1
        except IndexError:
            doneCounting = True
            break
    if doneCounting:
        sys.stdout.write("\n")
        break

end_time = time.time()
elapsed_time = end_time - start_time
print (str(elapsed_time) + " seconds to retrieve " + str(counter) + " followers")

#print followers

# LOAD OLD FOLLOWERS
oldfollowers = []
fo = open('old', 'r')
for line in fo:
    oldfollowers.append(line.strip())
fo.close()

fh = open('out', 'w')
for user in followers:
    fh.write(user+"\n")
fh.close()
