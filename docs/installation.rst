Installation
============

Cloudscraper OSSE is distributed in two forms :

* a single server app, which runs on your centralized machine (typically in-house server or any desktop) and handles global system settings
* node app, which you install and run on the other (non-server) machines to enable using data from them (desktops, laptops or other in-house servers)

Installing a single server app is sufficient for basic usage. If you want to search data from other (non-server) computers
as well, arbitrary node apps needs to be installed and set to communicate with the server. You manage your configuration
and nodes as with other settings - via administration panel available at /admin.

If you want to go distributed ie. install node apps as well, make sure nodes and server can see each other. This is easily achieved in your
home or office LAN, but sometimes you need to go beyond your network (aka over the intrnet). In this case make sure sufficient firewall
and router rules are properly set. To fetch data from other repositories (like public or your email servers, exchange and others), you do not
need to set anything more, except that you can access this server from your network.

First, make sure Python 2.7.x is properly installed and set, along with pip. Proceed with instructions `here <https://www.python.org/downloads/>`_.
On Linux, Python is probably already there, but it is highly recommended to install and set virtualenv. Instructions `are here <https://virtualenv.pypa.io/en/latest/>`_.

Note: virtualenv can be installed on Windows as well, but this approach is not covered at the moment.

*Make sure you do not mix os architecture and python versions - i.e. for 64-bit Windows, make sure you install 64-bit Python as well!*

Install Java 1.7+. It is optional but recommended to install JDK over JRE for performance reasons.

Additional requirements for Windows (any version) :

* Install Microsoft Visual C++ 2010 SP1 Redistributable Package `from here <http://www.microsoft.com/en-us/download/details.aspx?id=8328>`_

Install and set Apache 2.2.x or Nginx server with mod_wsgi. The following instructions will assume you have chosen Apache as your main deployment
server.

Unzip/copy Cloudscraper OSSE into desired folder on your hard drive. For best performance, put Cloudscraper OSSE on your SSD.

Assuming you have unpacked the source into the `c:\cloudscraper`, for Apache, edit `conf/httpd.conf` and add the following :

::

    ...
    LoadModule wsgi_module modules/mod_wsgi.so
    ...

    # cloudscraper
    WSGIScriptAlias / c:/cloudscraper/cloudscraper_osse/wsgi.py
    WSGIPythonPath c:/cloudscraper

    <Directory "c:/cloudscraper/cloudscraper_osse">
        <Files wsgi.py>
            Order deny,allow
            Allow from all
        </Files>
    </Directory>
