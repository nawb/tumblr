#!/usr/bin python
import os, sys, oauth2, urlparse, pytumblr, json, time
from difflib import context_diff
from unicodedata import normalize
from pprint import pprint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# GLOBAL VARIABLES
storageDir = '.saves/'

def getBlogUrl(blogurl=""):
    # CHECK FOR ARGV[1]
    try:
        blogurl = sys.argv[1]
    except:
        while not blogurl:
            sys.stderr.write("At least give me a blog URL: ")
            blogurl = str(raw_input(""))
    if not "." in blogurl:
        blogurl = blogurl+'.tumblr.com'
    return blogurl

blogurl = getBlogUrl()

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


setFollowers = set()
followers = []
counter = 0
offset = 0
doneCounting = False
firstLine = True
start_time = time.time()

while True:
    try:
        response = client.followers(blogurl, offset=offset)['users']
        if firstLine:
            firstLine = False
            sys.stdout.write("Retrieving followers")
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
        sys.stderr.write("\nYou gave me an incorrect blog! I have had it up to here with you honestly.\n")
        blogurl = getBlogUrl()
    except:
        sys.stdout.flush() #to clear output buffer
        sys.stderr.write("\nError retrieving. Try again in a minute.\n")
        exit()

end_time = time.time()
elapsed_time = end_time - start_time
print (str(elapsed_time) + " seconds to retrieve " + str(counter) + " followers")

# WRITE FOLLOWERS TO FILE
fh = open(storageDir+'out', 'w')
for user in followers:
    fh.write(user+"\n")
fh.close()

# If this is the first time this script is being run, there will be no old followers
if not os.path.exists(storageDir+'old'):
    sys.stdout.write("Thanks for using. :) "
                     + "We will have something for you the next time you run it.\n")
    exit()

# LOAD OLD FOLLOWERS
oldfollowers = []
fo = open(storageDir+'old', 'r')
for line in fo:
    line = line.strip()
    oldfollowers.append(line)
fo.close()
#print '\n'.join(oldfollowers)

## This will compare the two lists.
## it prints 5 lines of context around a change (unless it is near ends of file)
## shows a + for additions, - for deletions, ! for line changes
## The first two lines are useless

## Implementation note: urlchanges is special because we have an old url and the new url.
## We get both of those at separate, but consecutive lines. So once we hit one, 
## I set a toggle to wait for the next line which should contain the new URL.
newfollows, unfollows, urlchanges = [],[],[]
newurl = False
for line in context_diff(oldfollowers, followers):
    if line.startswith('+ '):
        newfollows.append(line.strip().split(' ')[1])
    if line.startswith('- '):
        unfollows.append(line.strip().split(' ')[1])
    if line.startswith('! '): 
        if newurl:
            templist.append(line.strip().split(' ')[1]) #add to existing list
            urlchanges.append(templist)
            newurl = False
        else:
            templist = list() #make new list
            templist.append(line.strip().split(' ')[1])
            newurl = True     #signal that next line is going to be new url

# DO THE PRINTING STUFF
if newfollows:
    sys.stdout.write(bcolors.OKGREEN + str(len(newfollows))
                     + " new cultists!!\n"
                     + bcolors.ENDC)
    temp = [sys.stdout.write(" %s," % (newfollower)) for newfollower in newfollows]
    sys.stdout.write("\b  \n") #sketchy way to erase the last comma
else:
    sys.stdout.write("No new people found you interesting.\n")
    
if unfollows:
    sys.stdout.write(bcolors.FAIL + str(len(unfollows)) 
                     + " have chosen to pursue a career in the landfill business." 
                     + " Nothin but a bunch of LOSERS!!\n"
                     + bcolors.ENDC)
    temp = [sys.stdout.write(" %s," % (unfollower)) for unfollower in unfollows]
    sys.stdout.write("\b  \n") #erase the last comma
else:
    sys.stdout.write("No one ran away from your stank. This must be your good week.\n")

if urlchanges:
    sys.stdout.write(bcolors.OKBLUE + str(len(urlchanges)) 
                     + " people changed their URL. Lord help us.\n" 
                     + bcolors.ENDC)
    temp = [sys.stdout.write("%13s -> %s\n" % (oldurl,newurl)) for oldurl,newurl in urlchanges]
    #13 is the average length of a url (based on scientific study done on my followers list)

print ""
