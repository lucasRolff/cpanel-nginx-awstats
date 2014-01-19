#!/usr/bin/python
import sys, pwd, grp, os
import simplejson as json

#Read the cpanel hook info from stdin
rawData = sys.stdin.readlines()

#We parse the json data using simplejson module
hookdata = json.loads(rawData[0])

data = hookdata['data']
username = data['user']
path = '/home/%s/tmp/awstats' % username
awstats_file = 'awstats.conf.include'

uid = pwd.getpwnam(username).pw_uid
gid = grp.getgrnam(username).gr_gid

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
ExtraTrackedRowsLimit=10000
"""

#Create a file and write the content
with open("%s/%s" % (path, awstats_file), 'w') as f:
    f.write(file_content)

def _chown(path, uid, gid):
    os.chown(path, uid, gid)
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        if os.path.isfile(itempath):
            os.chown(itempath, uid, gid)
        elif os.path.isdir(itempath):
            os.chown(itempath, uid, gid)
            self._chown(itempath, uid, gid)

#if the folder exist (it should, since we just created it) - then chown it to the user.
if os.path.exists(path):
    _chown(path, uid, gid)
