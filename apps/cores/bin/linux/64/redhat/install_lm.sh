#!/bin/sh
echo "Copying cloudscraper_lm init.d script into /etc/init.d ..." 
cp "$1"/bin/linux/64/redhat/cloudscraper_lm.init.d /etc/init.d/cloudscraper_lm
chmod +x /etc/init.d/cloudscraper_lm
echo "Calling chkconfig for cloudscraper_lm..."
chkconfig --level 2345 cloudscraper_lm on
