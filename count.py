#!/usr/bin python
import sys
import oauth2
import urlparse
import pytumblr
import json
import time
from unicodedata import normalize
from pprint import pprint

# CHECK FOR ARGV[1]
blogurl = ""
try:
    blogurl = sys.argv[1]
except:
    while not blogurl:
        blogurl = str(raw_input("Please enter your URL: "))
        if not "." in blogurl:
            blogurl = blogurl+'.tumblr.com'

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

setFollowers = set()
followers = []
counter = 0
offset = 0
doneCounting = False
start_time = time.time()

while True:
    try:
        response = client.followers(blogurl, offset=offset)['users']
        offset = offset + 20
        sys.stdout.flush() #to clear output buffer
        sys.stdout.write(".")
    
        for i in range(0,20):
            try:
                #extract name field and convert from unicode
                user = response[i]['name'].encode('ascii', 'ignore')
                if user not in setFollowers:
                    setFollowers.add(user)
                    followers.append(user)
                    counter = counter + 1
            except IndexError:
                doneCounting = True
                break
        if doneCounting:
            sys.stdout.write("\n")
            break
    except KeyError:
        sys.stdout.flush() #to clear output buffer
        sys.stderr.write("\nBlog not found\n")
        #call function to input again once functions are in place
        exit()

end_time = time.time()
elapsed_time = end_time - start_time
print (str(elapsed_time) + " seconds to retrieve " + str(counter) + " followers")

#print followers

# LOAD OLD FOLLOWERS
oldfollowers = []
fo = open('old', 'r')
for line in fo:
    line = line.strip()
    oldfollowers.append(line)
fo.close()
#print '\n'.join(oldfollowers)

joffset = 0

for i in range(0,counter):
    j = i + joffset
    while (j < counter and oldfollowers[i] != followers[j]):
    #    print followers[j]
        joffset = joffset + 1
        j = j + 1

fh = open('out', 'w')
for user in followers:
    fh.write(user+"\n")
#fh.write("Total: "+str(counter)+" followers.\n")
fh.close()
