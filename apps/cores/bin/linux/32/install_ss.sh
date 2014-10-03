#!/bin/sh
echo "Copying cloudscraper_ss init.d script into /etc/init.d ..." 
cp "$1"/lib/linux/32/cloudscraper_ss.init.d /etc/init.d/cloudscraper_ss
chmod +x /etc/init.d/cloudscraper_ss
echo "Calling sysv-rc-conf for cloudscraper_ss..."
sysv-rc-conf --level 2345 cloudscraper_ss on
