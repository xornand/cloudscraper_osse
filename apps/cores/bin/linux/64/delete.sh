#!/bin/sh
echo "Stopping cloudscraper service..."
service cloudscraper stop
update-rc.d -f cloudscraper remove
rm /etc/init.d/cloudscraper
