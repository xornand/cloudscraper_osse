#!/bin/sh
echo "Copying cloudscraper_lm init.d script into /etc/init.d ..." 
cp "$1"/lib/linux/32/cloudscraper_lm.init.d /etc/init.d/cloudscraper_lm
chmod +x /etc/init.d/cloudscraper_lm
echo "Calling sysv-rc-conf for cloudscraper_lm..."
sysv-rc-conf --level 2345 cloudscraper_lm on
