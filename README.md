cpanel-awstats-nginx-support
============================

#What is it for?
The script below is created, because some hosts decide to run custom webservers, like nginx, which might have a different log_format than apache have my default.

The reason why the code below is added to the `awstats.conf.include` file, is because the awstats in cpanel doesn't support it. So putting the LogFormat in the global awstats.conf, won't work, so it needs to be added on a user specific level.

The code below, is meant for the following log_format in nginx:
	
	log_format timed_combined '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_time';

#Adding hook

To add the hook into cPanel, you should use the code below:

	/usr/local/cpanel/bin/manage_hooks add script /opt/makeawstats/makeawstats.py --stage post --category Whostmgr --event Accounts::Create
	
In general what you do, is to add a script, to the post stage of the `Whostmgr::Accounts::Create` hook of cpanel, this will be run after the creation of a new account.

To take a small overview, of what the code does:

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
	f.write('ExtraTrackedRowsLimit=10000\n')
	f.close()

	if os.path.exists('/home/%s/tmp/awstats' % username):
	    os.system('chown -R %s:%s /home/%s/tmp/awstats' % (username, username, username))

	
Above, you can see the code (located in makeawstats folder).

When reading from stdin, you'll get a json string returned, due to the lack of json module in Python2.4 which is default on CentOS 5.x systems, we're using eval instead, and we do some replacement of `':null'` to `':None'`.

It makes a file in the `/home/$USER/tmp/awstats/awstats.conf.include`, and writing the custom logformat to that file, and at same time it adds a section into awstats displaying the information from `%extra1`.
