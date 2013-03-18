#!/usr/bin/python
import sys, os

#Read the cpanel hook info from stdin
rawData = sys.stdin.readlines()

#Replace null with None, since the default python2.4 (centos 5)
#doesn't have json module, we can work around it like that
hookdata = eval(rawData[0].replace(':null', ':None'))

data = hookdata['data']
username = data['user']

#if the awstats folder doesn't exist in the users tmp folder, then create it
if not os.path.exists('/home/%s/tmp/awstats' % username):
    os.makedirs('/home/%s/tmp/awstats' % username)

#Create a file, and write the content
f = open('/home/%s/tmp/awstats/awstats.conf.include' % username, 'w')
f.write('LogFormat="%host %other %logname %time1 %methodurl %code %bytesd %refererquot %uaquot %extra1"\n')
f.write('ExtraSectionName1="Time to serve requests (seconds)"\n')
f.write('ExtraSectionCodeFilter1=""\n')
f.write('ExtraSectionFirstColumnTitle1="Number of seconds to serve the request"\n')
f.write('ExtraSectionFirstColumnValues1="extra1,(.*)"\n')
f.write('ExtraSectionStatTypes1="H"\n')
f.write('ExtraTrackedRowsLimit=10000\n')
f.close()

#if the folder exist (it should, since we just created it) - then chown it to the user.
if os.path.exists('/home/%s/tmp/awstats' % username):
    os.system('chown -R %s:%s /home/%s/tmp/awstats' % (username, username, username))
