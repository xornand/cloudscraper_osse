#!/bin/sh
echo "Stopping cloudscraper ss service..."
service cloudscraper_ss stop
chkconfig --del cloudscraper_ss
rm /etc/init.d/cloudscraper_ss
