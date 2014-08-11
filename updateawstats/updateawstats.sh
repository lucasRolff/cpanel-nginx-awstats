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