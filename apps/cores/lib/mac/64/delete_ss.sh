#!/bin/sh
echo "Stopping cloudscraper ss service..."
service cloudscraper_ss stop
update-rc.d -f cloudscraper_ss remove
rm /etc/init.d/cloudscraper_ss
