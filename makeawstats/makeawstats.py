#!/usr/bin/python
import sys, os

rawData = sys.stdin.readlines()

hookdata = eval(rawData[0].replace(':null', ':None'))

data = hookdata['data']
username = data['user']

if not os.path.exists('/home/%s/tmp/awstats' % username):
    os.makedirs('/home/%s/tmp/awstats' % username)

f = open('/home/%s/tmp/awstats/awstats.conf.include' % username, 'w')
f.write('LogFormat="%host %other %logname %time1 %methodurl %code %bytesd %refererquot %uaquot %extra1"\n')
f.write('ExtraSectionName1="Time to serve requests (seconds)"\n')
f.write('ExtraSectionCodeFilter1=""\n')
f.write('ExtraSectionFirstColumnTitle1="Number of seconds to serve the request"\n')
f.write('ExtraSectionFirstColumnValues1="extra1,(.*)"\n')
f.write('ExtraSectionStatTypes1="H"\n')
f.close()

if os.path.exists('/home/%s/tmp/awstats' % username):
    os.system('chown -R %s:%s /home/%s/tmp/awstats' % (username, username, username))
