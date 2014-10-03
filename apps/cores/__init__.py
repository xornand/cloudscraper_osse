# startup code
# if you put this code inside __init__.py for cores app, it will get loaded twice, but that's only
# if you start runserver...for normal deployments it's ok!
# To avoid calling twice :
# - put this code in wsgi.py
# - use runserver --noreload
# TODO: check with lazy loading of apps!

import logging
logger = logging.getLogger(__name__)

f1 = None
sched = None

from ctypes import *
import os

from subprocess import call
import atexit

from cores.models import Ranking
from cloudscraper_osse.utils import is_windows, is_linux, is_python_32bit, info, is_os_64bit
from django.conf import settings
from cores.models import Core
from django.contrib.auth.models import User

import sys

def startupEngine():

    # we have to do this because we have two DLLs and
    # and the first one will search for the second in the current
    # dir. Since the current dir is project root, it will fail if we
    # do not set this
    #os.chdir("C:/Users/Vojislav/Django/cloudscraper/apps/cores");
    dirpath = os.path.dirname(os.path.realpath(__file__))
    #os.chdir(dirpath)
    
    logger.info(info())
    
    # detect os and Python and load appropriate library
    if is_windows():
        if not is_os_64bit():
            os.environ['PATH'] = os.path.join(dirpath, 'lib','windows','32') + ';' + os.environ['PATH']
            lib = cdll.LoadLibrary("lucene++.dll")
        else:
            if is_python_32bit():
                logger.warn('You are using 32-bit python on 64-bit system!')
                os.environ['PATH'] = os.path.join(dirpath, 'lib','windows','32') + ';' + os.path.join(dirpath, 'lib','windows','64') + ';' + os.environ['PATH']
                lib = cdll.LoadLibrary("lucene++.dll")
            else:
                os.environ['PATH'] = os.path.join(dirpath, 'lib','windows','64') + ';' + os.environ['PATH']
                lib = cdll.LoadLibrary("lucene++64.dll")
    elif is_linux():
        if not is_os_64bit():
            #os.environ['PATH'] = os.path.join(dirpath, 'lib','linux','32') + ';' + os.environ['PATH']
            #lib = cdll.LoadLibrary("liblucene++.so.3.0.6")
            os.chdir(os.path.join(dirpath, 'lib','linux','32'))
            lib = cdll.LoadLibrary("./liblucene++.so.3.0.6")
        else:
            #os.environ['PATH'] = os.path.join(dirpath, 'lib','linux','64') + ';' + os.environ['PATH']
            #lib = cdll.LoadLibrary("liblucene++.so.3.0.6")
            os.chdir(os.path.join(dirpath, 'lib','linux','64'))
            lib = cdll.LoadLibrary("./liblucene++.so.3.0.6")
    elif is_mac():
        logger.error("mac not supported at the moment")
        return
    else:
        logger.error("Unable to detect os and platform!")
        return
        

    lib.newFacade.restype = c_void_p

    lib.deleteFacade.argtypes = [c_void_p]
    lib.deleteFacade.restype = c_void_p

    lib.initFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
    lib.initFacade.restype = c_void_p

    lib.closeFacade.argtypes = [c_void_p]
    lib.closeFacade.restype = c_void_p

    lib.indexFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, POINTER(c_int), c_int]
    lib.indexFacade.restype = c_void_p

    lib.searchFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_int, c_int, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_int, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p]
    lib.searchFacade.restype = c_void_p

    lib.suggestFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_int, c_int]
    lib.suggestFacade.restype = c_void_p

    lib.commitFacade.argtypes = [c_void_p]
    lib.commitFacade.restype = c_void_p
    
    lib.optimizeFacade.argtypes = [c_void_p]
    lib.optimizeFacade.restype = c_void_p
    
    lib.addRankingFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_int, c_int, c_int]
    lib.addRankingFacade.restype = c_void_p
    
    lib.removeRankingFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
    lib.removeRankingFacade.restype = c_void_p
    
    lib.getSizeInMibFacade.argtypes = [c_void_p]
    lib.getSizeInMibFacade.restype = c_double
    
    lib.getDocNumFacade.argtypes = [c_void_p, c_wchar_p]
    lib.getDocNumFacade.restype = c_long

    class Facade(object):

        def __init__(self):
            self.obj = lib.newFacade()

        def init(self, path, core):
            return lib.initFacade(self.obj, path, core)

        def close(self):
            return lib.closeFacade(self.obj)

        def delete(self):
            return lib.deleteFacade(self.obj)

        def index(self, hostname, port, path, facet, uidsArr, uidsSize):
            return lib.indexFacade(self.obj, hostname, port, path, facet, uidsArr, uidsSize)

        def search(self, q, start, hitsPerPage, sort, order, mode, facet, uid, df, dfFrom, dfTo, lf, lfl, ff, ffct):
            dst = create_unicode_buffer(10000) # initial capacity 10000
            dst[0] = u"\u0000"
            lib.searchFacade(self.obj, dst, q, start, hitsPerPage, sort, order, mode, facet, uid, df, dfFrom, dfTo, lf, lfl, ff, ffct)
            return dst.value

        def suggest(self, q, n, uid):
            dst = create_unicode_buffer(10000) # initial capacity 10000
            dst[0] = u"\u0000"
            lib.suggestFacade(self.obj, dst, q, n, uid)
            return dst.value
        
        def commit(self):
            return lib.commitFacade(self.obj)
        
        def optimize(self):
            return lib.optimizeFacade(self.obj)
        
        def add_ranking(self, title, q, docid, resno, uid):
            return lib.addRankingFacade(self.obj, title, q, docid, resno, uid)
        
        def remove_ranking(self, title, q):
            return lib.removeRankingFacade(self.obj, title, q)
        
        def get_size(self):
            return lib.getSizeInMibFacade(self.obj)
        
        def get_doc_num(self, facet):
            return lib.getDocNumFacade(self.obj, facet)

    global f1
    f1 = Facade()
    # it is assumed that cores dir exists!
    # if you want to create a new index, index folder must NOT exist!
    c1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cores")
    
    
    #add default index record into db
    defaultdir = os.path.join(c1, 'default')
    #if not os.path.exists(defaultdir):
        #logger.info('Default core did not exist. Adding record into the db')
        #defaultcore = Core(title='default', description='Default core (index). Cannot be deleted', path=defaultdir)
        #defaultcore.save()
        
    # we only need to set path
    defaultcore = Core.objects.get(pk=1)
    if defaultcore.path == "unknown":
        defaultcore.path = defaultdir
        defaultcore.save(update_fields=['path'])
    
    #add default user (admin)
    #if "runserver" not in sys.argv:
        #User.objects.create_superuser(username="admin", email="bratislav1983@gmail.com", password="admin")
        #logger.info("Default superuser added")
    
    # this will create dir if it does not exist automatically
    f1.init(c1, "default")

# my shutdown hook
def shutdownEngine():
    global f1
    f1.close()
    f1.delete()

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.executors.pool import ThreadPoolExecutor

# def tick():
    # print "tick..."

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore

# apscheduler.standalone MUST BE FALSE!!!
def startupScheduler():
    configure = {
        'apscheduler.standalone': False,
        'apscheduler.jobstore.default.class': 'apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore',
        'apscheduler.jobstore.default.url': 'sqlite:///scheduler.sqlite3',
        'apscheduler.jobstore.default.tablename': 'apscheduler_jobs'
    }
    global sched
    sched = Scheduler(configure)
    sched.start()
    # sched.add_interval_job(tick, seconds=3)
    logger.info("Scheduler started")

def shutdownScheduler():
    global sched
    sched.shutdown(wait=False)
    logger.info("Scheduler stopped")

def startupServices():
    
    dirpath = os.path.dirname(os.path.realpath(__file__))
    
    if is_windows():
        if not is_os_64bit():
            os.environ['PATH'] = os.path.join(dirpath, 'bin','windows','32') + ';' + os.environ['PATH']
            logger.info("Starting Tika service...")
            call(["start.cmd"])
            logger.info("Starting Suggest service...")
            call(["start_ss.cmd"])
            if not settings.IS_OSS_VERSION:
                logger.info("Starting License service...")
                call(["start_lm.cmd"])
        else:
            os.environ['PATH'] = os.path.join(dirpath, 'bin','windows','64') + ';' + os.environ['PATH']
            logger.info("Starting Tika service (64-bit)...")
            call(["start64.cmd"])
            logger.info("Starting Suggest service (64-bit)...")
            call(["start64_ss.cmd"])
            if not settings.IS_OSS_VERSION:
                logger.info("Starting License service (64-bit)...")
                call(["start64_lm.cmd"])
    elif is_linux():
        if not is_os_64bit():
            pass
        else:
            pass
            
    elif is_mac():
        logger.error("mac not supported at the moment")
        return
    else:
        logger.error("Unable to detect os and platform!")
        return

def shutdownServices():
    # no need to stop services
    pass
    #logger.info("Stopping Tika service...")
    #call(["stop64.cmd"])
    #logger.info("Stopping Suggest service...")
    #call(["stop64_ss.cmd"])
    #logger.info("Stopping License service...")
    #call(["stop64_lm.cmd"])

def loadRankings():
    rankings = Ranking.objects.all()
    for r in rankings:
        global f1
        f1.add_ranking(r.title, r.query, r.docid, r.resno, 0)


if "syncdb" not in sys.argv and "collectstatic" not in sys.argv and "dbshell" not in sys.argv and "shell" not in sys.argv and "dumpdata" not in sys.argv and "loaddata" not in sys.argv:
    
    # no need to check if f1 is None
    startupEngine()
    startupScheduler()
    startupServices()
    loadRankings()
    
    # register shutdown hooks
    atexit.register(shutdownServices)
    atexit.register(shutdownScheduler)

    # works for Ctrl+C, not Ctrl+Break!
    atexit.register(shutdownEngine)

# end of startup code