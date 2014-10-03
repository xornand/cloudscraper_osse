Cloudscraper OSSE
=================

The Python/C++ search engine with a Google-like frontend and Wordpress-like backend.

Overview
--------

Cloudscraper OSSE is a _partially_ open source search engine which tries to recreate Google search experience on top of your personal or enterprise data. It provides a full-text and full-metadata search and complete management of your accounts from where data can be fetched from. Cloudscraper OSSE is compatibible with the most common file types and servers and is designed to run on a commodity hardware. It was designed to be simple so anyone in your family or in the office can use it.

_This software is still under development and may still contain bugs. Please do not use this software with your sensitive data at this stage_ 

Set your in-house, private or public Google-like search in a few minutes:

![Cloudscraper OSSE frontend](https://raw.github.com/bratislav/cloudscraper_osse/github/docs/images/cloudscraper-osse-fe.png "Cloudscraper OSSE")
![Cloudscraper OSSE backend](https://raw.github.com/bratislav/cloudscraper_osse/github/docs/images/cloudscraper-osse-be.png "Cloudscraper OSSE")

Cloudscraper OSSE is a core of a more robust and commercial enterprise search engine called [Cloudscraper ESE](http://www.cloudscraper.ca/). 

Features
--------
* platform neutral, lightweight and fast - get results in less than second
* smaller memory consumption in comparison to Apache Solr/SolrCloud and other Java Lucene based engines
* scalable up to GiB of documents
* Google-like experience and Wordpress-like administration
* full-text and full-metadata search based on the excellent [luceneplusplus](https://github.com/luceneplusplus/LucenePlusPlus)
* support for multiple indices - easily backup/connect the index you want
* support for Apache Solr/SolrCloud indices - easily import existing index via Import plugin
* support for Elasticsearch indices
* support for common file types like PDF, Microsft Office, OpenOffice.org and others
* support for local & remote directories, email servers (pop3/imap), Gmail
* support for Dropbox & Google Drive
* customizable results and suggestions (auto-complete) based on the currently logged in user
* search result rankings customization
* search support via mobile devices (Android, iPhone, iPad)
* easy integration with existing software that was designed to work with Apache Solr/Elasticsearch
* easy integration with other systems via REST API
* extensible via plugins

Support for Microsft Exchange 2003-2013, Android and iOS data and others is available int the
commercial version available at [Cloudscraper ESE](http://www.cloudscraper.ca/). Differences between OSSE i ESE versions can
be viewed [here](http://www.cloudscraper.ca/).

Requirements
------------

Cloudscraper OSSE requires the following:

* Python 2.7.x
* Java 1.6+ (Windows) or Java 1.7+ (non-Windows) (tested under Oracle's HotSpot and OpenJDK 1.7)
* Microsoft Visual C++ 2010 SP1 Redistributable Package (for Windows only)
* libicu-dev (non-Windows only)

Installation
------------

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

First, make sure Python 2.7.x is properly installed and set, along with pip. Proceed with instructions [here](https://www.python.org/downloads/).
On Linux, Python is probably already there, but it is highly recommended to install and set virtualenv. Instructions [here](https://virtualenv.pypa.io/en/latest/).

Note: virtualenv can be installed on Windows as well, but this approach is not covered at the moment.

*Make sure you do not mix os architecture and python versions - i.e. for 64-bit Windows, make sure you install 64-bit Python as well!*

Install Java 1.7+. It is optional but recommended to install JDK over JRE for performance reasons.

Additional requirements for Windows (any version) :

* Install Microsoft Visual C++ 2010 SP1 Redistributable Package from [here](http://www.microsoft.com/en-us/download/details.aspx?id=8328)

Install and set Apache 2.2.x or Nginx server with mod_wsgi. The following instructions will assume you have chosen Apache as your main deployment
server.

Unzip/copy Cloudscraper OSSE into desired folder on your hard drive. For best performance, put Cloudscraper OSSE on your SSD.

Assuming you have unpacked the source into the `c:\cloudscraper`, for Apache, edit `conf/httpd.conf` and add the following :

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


Usage
-----


Cloudscraper OSSE shows its full power if you want to search your data and you remember at least
one keyword (you don't have to remember it correctly), but you can't remember :

- where did you save that document
- what is the type of your document (whether it's file, email, database record or somewhere in your cloud storage)
- what's the file format of you document
- who's the author etc.

Cloudscraper OSSE abstracts this searching process so you only have to type what you remember and leave the other to
the software. This becomes especially handy if you have a lot of data!

At this point you system is ready for crawling and searching, but it's empty.

Power up your wsgi web server and proceed with the initial setup. Open you browser and
go to [http://127.0.0.1/adminpanel](http://127.0.0.1/adminpanel). Login with the default username `admin` and password
`admin`. Do not forget to change this later via Administration->auth->users page for security reasons!

Let's add a single directory which resides on your local drive (on the same machine where you installed Cloudscraper OSSE).

Open [http://127.0.0.1/adminpanel/locals/directory](http://127.0.0.1/adminpanel/locals/directory) and click on `Add`. Enter
a non-empty directory path, and choose one of the predefined schedules. If you're not satisfied with them, you can always create
new ones on the cores->schedules page ordirectly by clicking on the + button. Additionaly, set description, owner and permissions
and click on `Save`. After a few moments (depends on directory size), your index will be ready for searching.

At this time your directory is added into the system and it will be crawled and updated by the schedule you have set during creation.

Documentation & Support
-----------------------

Full documentation for the project is available at [http://cloudscraper-osse.readthedocs.org](http://cloudscraper-osse.readthedocs.org).

For questions and support, use the [Cloudscraper discussion group](https://groups.google.com/forum/#!forum/cloudscraper_osse), or `#cloudscraper` on freenode IRC.

You may also want to [follow the author on Twitter](http://www.twitter.com).

License
-------

Copyright (c) 2013-2014, Bratislav Stojanovic. All rights reserved.

Please read LICENSE file.

Acknowledgements
----------------

Alan Wright, the creator of the LucenePlusPlus (up to date C++ port of the Lucene library)

