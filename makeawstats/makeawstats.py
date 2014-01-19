#!/usr/bin/python
import sys, os
from subprocess import Popen
import simplejson as json

#Read the cpanel hook info from stdin
rawData = sys.stdin.readlines()

#We parse the json data using simplejson module
hookdata = json.loads(rawData[0])

data = hookdata['data']
username = data['user']
path = '/home/%s/tmp/awstats' % username
awstats_file = 'awstats.conf.include'

#if the awstats folder doesn't exist in the users tmp folder, then create it
if not os.path.exists(path):
    os.makedirs(path)

file_content = """\
LogFormat="%host %other %logname %time1 %methodurl %code %bytesd %refererquot %uaquot %extra1"
ExtraSectionName1="Time to serve requests (seconds)"
ExtraSectionCodeFilter1=""
ExtraSectionFirstColumnTitle1="Number of seconds to serve the request"
ExtraSectionFirstColumnValues1="extra1,(.*)"
ExtraSectionStatTypes1="H"
ExtraTrackedRowsLimit=100000
"""

#Create a file and write the content
with open("%s/%s" % (path, awstats_file), 'w') as f:
    f.write(file_content)

#if the folder exist (it should, since we just created it) - then chown it to the user.
if os.path.exists(path):
    Popen("chown -R %s. %s" % (username, path), shell=True)