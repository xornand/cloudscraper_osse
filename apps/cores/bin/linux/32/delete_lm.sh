#!/bin/sh
echo "Stopping cloudscraper lm service..."
service cloudscraper_lm stop
update-rc.d -f cloudscraper_lm remove
rm /etc/init.d/cloudscraper_lm
