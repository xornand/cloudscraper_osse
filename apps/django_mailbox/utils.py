import email.header
import logging

import six

from django.conf import settings
import cores

from urlparse import urlparse
from django.conf import settings
import os

from ctypes import *

logger = logging.getLogger(__name__)


DEFAULT_CHARSET = getattr(
    settings,
    'DJANGO_MAILBOX_DEFAULT_CHARSET',
    'iso8859-1',
)


def convert_header_to_unicode(header):
    def _decode(value, encoding):
        if isinstance(value, six.text_type):
            return value
        if not encoding or encoding == 'unknown-8bit':
            encoding = DEFAULT_CHARSET
        return value.decode(encoding, 'REPLACE')

    try:
        return ''.join(
            [
                (
                    _decode(bytestr, encoding)
                ) for bytestr, encoding in email.header.decode_header(header)
            ]
        )
    except UnicodeDecodeError:
        logger.exception(
            'Errors encountered decoding header %s into encoding %s.',
            header,
            DEFAULT_CHARSET,
        )
        return unicode(header, DEFAULT_CHARSET, 'replace')

def crawl_global(curmodel):
    
    logger.info("Crawling %s started" % curmodel.name)
    
    # taken from get_new_mail body 
    logger.debug('Receiving mail for %s' % curmodel)
    curmodel.get_new_mail()
    
    # index eml files
    # parse from uri hostname, port and path
    
    pres = urlparse(curmodel.uri)
    
    port = 110
    if pres.port is not None:
        port = pres.port
    else:
        if pres.hostname.startswith('imap'):
            port = 143
    
    # todo: check if there are any more default port values other than pop3 and imap (no ssl)
    
    #print pres.hostname
    #print port
    #print os.path.join(settings.BASE_DIR, 'apps', 'cores', 'incoming', 'django_mailbox', curmodel.name)
    #print type(os.path.join(settings.BASE_DIR, 'apps', 'cores', 'incoming', 'django_mailbox', curmodel.name))
    
    nusers = curmodel.users.count()
    print "Num of users is %d" % nusers
    
    #uidsArray = (c_int * 1)()
    #uidsArray[0] = 1
    
    if nusers == 0:
        uidsArray = (c_int * 1)()
    else:
        uidsArray = (c_int * nusers)()
    
    if nusers == 0:
        uidsArray[0] = 0
        print "uidsArray[0] = 0"
    else:
        for i in range(nusers):
            uidsArray[i] = curmodel.users.all()[i].id
            print "uidsArray[%d] = %d" % (i, curmodel.users.all()[i].id)
    
    #cores.f1.index(pres.hostname, unicode(port), os.path.join(settings.BASE_DIR, 'apps', 'cores', 'incoming', 'django_mailbox', curmodel.name), 'email', 1)
    cores.f1.index(pres.hostname, unicode(port), os.path.join(settings.BASE_DIR, 'apps', 'cores', 'incoming', 'django_mailbox', curmodel.name), 'email', uidsArray, len(uidsArray))
    
    # index attachments
    logger.info('Indexing attachments')
    #cores.f1.index(pres.hostname, unicode(port), os.path.join(settings.BASE_DIR, 'apps', 'cores', 'incoming', 'django_mailbox', curmodel.name, 'attachments'), 'file', 1)
    cores.f1.index(pres.hostname, unicode(port), os.path.join(settings.BASE_DIR, 'apps', 'cores', 'incoming', 'django_mailbox', curmodel.name, 'attachments'), 'file', uidsArray, len(uidsArray))
    
    cores.f1.commit()
    
    logger.info("Crawling %s completed successfully" % curmodel.name)
    
    
