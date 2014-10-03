#!/bin/sh
echo "Copying cloudscraper_ss init.d script into /etc/init.d ..." 
cp "$1"/bin/linux/64/redhat/cloudscraper_ss.init.d /etc/init.d/cloudscraper_ss
chmod +x /etc/init.d/cloudscraper_ss
echo "Calling chkconfig for cloudscraper_ss..."
chkconfig --level 2345 cloudscraper_ss on
