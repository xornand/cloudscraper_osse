#!/bin/sh
echo "Copying cloudscraper init.d script into /etc/init.d ..." 
cp "$1"/bin/linux/64/redhat/cloudscraper.init.d /etc/init.d/cloudscraper
chmod +x /etc/init.d/cloudscraper
echo "Calling chkconfig for cloudscraper..."
chkconfig --level 2345 cloudscraper on
