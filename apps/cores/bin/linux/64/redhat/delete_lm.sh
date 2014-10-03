#!/bin/sh
echo "Stopping cloudscraper lm service..."
service cloudscraper_lm stop
chkconfig --del cloudscraper_lm
rm /etc/init.d/cloudscraper_lm
