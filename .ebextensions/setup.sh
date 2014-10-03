#!/bin/bash

# instructions from http://www.hudku.com/blog/configuration-setup-customizing-aws-elastic-beanstalk/

# Get the directory of 'this' script
dirApp=$(dirname "${BASH_SOURCE[0]}")
echo "current dir is $dirApp"

# current user is root!
#echo "what user runs the apache?"
#ps axo user,group,comm | grep apache

# Set permissions
chmod 777 $dirApp/../
#chmod 777 $dirApp/../apps/
#chmod 777 $dirApp/../apps/cores/
chmod 777 $dirApp/../db.sqlite3
chmod 777 $dirApp/../cloudscraper.log
chmod 777 $dirApp/../scheduler.sqlite3

chown apache.apache $dirApp/../
chown apache.apache $dirApp/../db.sqlite3
chown apache.apache $dirApp/../cloudscraper.log
#chown apache.apache $dirApp/../apps/
#chown apache.apache $dirApp/../apps/cores/
chown apache.apache $dirApp/../scheduler.sqlite3

#ls -la

cd $dirApp/../apps/cores
ls -la

# set executable permissions for linux scripts
chmod 775 $dirApp/../apps/cores/linux/64/install.sh
chmod 775 $dirApp/../apps/cores/linux/64/install_lm.sh
chmod 775 $dirApp/../apps/cores/linux/64/install_ss.sh
chmod 775 $dirApp/../apps/cores/linux/64/start.sh
chmod 775 $dirApp/../apps/cores/linux/64/start_lm.sh
chmod 775 $dirApp/../apps/cores/linux/64/start_ss.sh
chmod 775 $dirApp/../apps/cores/linux/64/stop.sh
chmod 775 $dirApp/../apps/cores/linux/64/stop_lm.sh
chmod 775 $dirApp/../apps/cores/linux/64/stop_ss.sh
chmod 775 $dirApp/../apps/cores/linux/64/delete.sh
chmod 775 $dirApp/../apps/cores/linux/64/delete_lm.sh
chmod 775 $dirApp/../apps/cores/linux/64/delete_ss.sh
chmod 775 $dirApp/../apps/cores/linux/64/cloudscraper
chmod 775 $dirApp/../apps/cores/linux/64/cloudscraper_lm
chmod 775 $dirApp/../apps/cores/linux/64/cloudscraper_ss

# Print the finish time of this script
echo $(date)
  
  
# Always successful exit so that beanstalk does not stop creating the environment
exit 0
