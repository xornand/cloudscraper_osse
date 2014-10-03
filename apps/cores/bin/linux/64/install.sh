#!/bin/sh
echo "Copying cloudscraper init.d script into /etc/init.d ..." 
cp "$1"/lib/linux/64/cloudscraper.init.d /etc/init.d/cloudscraper
chmod +x /etc/init.d/cloudscraper
echo "Calling sysv-rc-conf for cloudscraper..."
sysv-rc-conf --level 2345 cloudscraper on
