#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Example from http://stackoverflow.com/questions/17244756/python-ctypes-wraping-c-class-with-operators

from ctypes import *
import os

lib = cdll.LoadLibrary("lucene++.dll")

lib.newFacade.restype = c_void_p

lib.deleteFacade.argtypes = [c_void_p]
lib.deleteFacade.restype = c_void_p

lib.initFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
lib.initFacade.restype = c_void_p

lib.closeFacade.argtypes = [c_void_p]
lib.closeFacade.restype = c_void_p

lib.indexFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_wchar_p]
lib.indexFacade.restype = c_void_p

lib.searchFacade.argtypes = [c_void_p, c_wchar_p, c_int, c_int, c_wchar_p, c_wchar_p, c_wchar_p, c_int, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p]
lib.searchFacade.restype = c_void_p

lib.suggestFacade.argtypes = [c_void_p, c_wchar_p]
lib.suggestFacade.restype = c_void_p

lib.optimizeFacade.argtypes = [c_void_p]
lib.optimizeFacade.restype = c_void_p

class Facade(object):

    def __init__(self):
        self.obj = lib.newFacade()

    def init(self, path, core):
        return lib.initFacade(self.obj, path, core)

    def close(self):
        return lib.closeFacade(self.obj)

    def delete(self):
        return lib.deleteFacade(self.obj)

    def index(self, hostname, port, path):
        return lib.indexFacade(self.obj, hostname, port, path)

    def search(self, q, start, hitsPerPage, sort, mode, facet, uid, df, lf, lfl, ff, ffct):
        return lib.searchFacade(self.obj, q, start, hitsPerPage, sort, mode, facet, uid, df, lf, lfl, ff, ffct)

    def suggest(self, q):
        return lib.suggestFacade(self.obj, q)
    
    def optimize(self):
        return lib.optimizeFacade(self.obj)

        
f1 = Facade()
# it is assumed that cores dir exists!
# if you want to create a new index, index folder must NOT exist!
c1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cores")
f1.init(c1, "default")

#it is assumed that output dir exists!
f1.index("127.0.0.1", "8000", "c:/Users/Bratislav/Downloads/tests")
#f1.optimize()
#f1.search(u"123šđčćŠĐČĆ")
f1.search(u"123", 1, 10, u"", u"cm", u"", 0, u"", u"", u"", u"", u"")
f1.suggest(u"123")

f1.close()
f1.delete()