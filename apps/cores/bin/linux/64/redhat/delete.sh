#!/bin/sh
echo "Stopping cloudscraper service..."
service cloudscraper stop
chkconfig --del cloudscraper
rm /etc/init.d/cloudscraper
