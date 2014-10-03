.. Cloudscraper OSSE documentation master file, created by
   sphinx-quickstart on Wed Sep 17 11:52:38 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cloudscraper OSSE's documentation
=================================

Introduction
------------

Cloudscraper OSSE is a open source search engine which tries to recreate Google search experience on top of your personal or enterprise data.
It provides a full-text and full-metadata search and complete management of your accounts from where data can be fetched from.
Cloudscraper OSSE is compatibible with the most common file types and servers and is designed to run on a commodity hardware.
It was designed to be simple so anyone in your family or in the office can use it.

*This software is still under development and may still contain bugs. Please do not use this software with your sensitive data at this stage.*

Set your in-house, private or public Google-like search in a few minutes:

.. image:: /images/cloudscraper-osse-fe.png
    :height: 400px
    :width: 600px
    :scale: 100%
    :alt: Cloudscraper OSSE front-end

.. image:: /images/cloudscraper-osse-be.png
    :height: 400px
    :width: 600px
    :scale: 100%
    :alt: Cloudscraper OSSE back-end

Cloudscraper OSSE is a core of a more robust and commercial enterprise search engine called `Cloudscraper ESE <http://www.cloudscraper.ca/>`_.

Features
--------

* platform neutral, lightweight and fast - get results in less than second
* smaller memory consumption in comparison to Apache Solr/SolrCloud and other Java Lucene based engines
* scalable up to GiB of documents
* Google-like experience and Wordpress-like administration
* full-text and full-metadata search based on the excellent `luceneplusplus <https://github.com/luceneplusplus/LucenePlusPlus>`_
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
commercial version available at `Cloudscraper ESE <http://www.cloudscraper.ca/>`_. Differences between OSSE i ESE versions can
be viewed `here <http://www.cloudscraper.ca/>`_.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   requirements
   installation
   usage
   faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

