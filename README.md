cpanel-awstats-nginx-support
============================

#What is it for?
The script below is created, because some hosts decide to run custom webservers, like nginx, which might have a different log_format than apache have by default.

The reason why the code below is added to the `awstats.conf.include` file, is because the awstats in cpanel doesn't support it. So putting the LogFormat in the global awstats.conf, won't work, so it needs to be added on a user specific level.

The code below, is meant for the following log_format in nginx:
	
	log_format timed_combined '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_time';

#Adding hook

To add the hook into cPanel, you should use the code below:

``` bash
/usr/local/cpanel/bin/manage_hooks \
add script /opt/makeawstats/makeawstats.py \
--stage post \
--category Whostmgr \
--event Accounts::Create \
--manual
```
	
In general what you do, is to add a script, to the post stage of the `Whostmgr::Accounts::Create` hook of cpanel, this will be run after the creation of a new account.

To take a small overview, of what the code does:



``` python
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

```

	
Above, you can see the code (located in makeawstats folder).

The cPanel hook system will return a json string that we can read from stdin, so we use simplejson (It's included in the repository) to do this. After this we parse the json data, and assign some variables.

It will make a file in the `/home/$USER/tmp/awstats` folder called `awstats.conf.include` and write the custom logformat, and the section name etc.

After this we recursively chown the folder and files to the user.


#Already have active cpanel users?

``` bash
#!bin/bash

CPANEL_USERS="ls /var/cpanel/users/"

for user in `$CPANEL_USERS`; do
AWSTATS_PATH="/home/$user/tmp/awstats/awstats.conf.include"
if [ ! -f $AWSTATS_PATH ]; then
echo "AWStats file not found for user: $user. Creating.."
# Inserting code to awstats.conf.include
echo '
LogFormat="%host %other %logname %time1 %methodurl %code %bytesd %refererquot %uaquot %extra1"
ExtraSectionName1="Time to serve requests (seconds"
ExtraSectionCodeFilter1=""
ExtraSectionFirstColumnTitle1="Number of seconds to serve the request"
ExtraSectionFirstColumnValues1="extra1,(.*"
ExtraSectionStatTypes1="H"
ExtraTrackedRowsLimit=100000' >> $AWSTATS_PATH
# Setting the right permissions for each user
chown -R $user:$user $AWSTATS_PATH
else
	echo "AWStats file found for user: $user. Doing nothing."
fi
done
```

Above, you can see the code (located in updateawstats folder).

Run the updateawstats.sh to loop through all cpanel users to check if they have the awstats.conf.include file. If not, the file gets created and populated with code.