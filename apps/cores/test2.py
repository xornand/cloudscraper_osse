# Example from http://stackoverflow.com/questions/17244756/python-ctypes-wraping-c-class-with-operators

from ctypes import *
import os

lib = cdll.LoadLibrary("lucene++.dll")

lib.newFacade.restype = c_void_p

lib.newFacade.restype = c_void_p

lib.deleteFacade.argtypes = [c_void_p]
lib.deleteFacade.restype = c_void_p

lib.initFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
lib.initFacade.restype = c_void_p

lib.closeFacade.argtypes = [c_void_p]
lib.closeFacade.restype = c_void_p

lib.indexFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_wchar_p]
lib.indexFacade.restype = c_void_p

lib.searchFacade.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_int, c_int, c_wchar_p, c_wchar_p, c_wchar_p, c_int, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p]
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
        dst = create_unicode_buffer(100000) # writable, unlike u"example".
        dst[0] = u"\u0000"
        lib.searchFacade(self.obj, dst, q, start, hitsPerPage, sort, mode, facet, uid, df, lf, lfl, ff, ffct)
        #print dst.value
        return dst

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


f1 = Facade()
f1.init(r"c:\Users\Vojislav\Django\cloudscraper\apps\cores\cores", "default")

#dst = create_unicode_buffer(10000) # writable, unlike u"example".
#dst[0] = u"\u0000"
#f1.search(u"123", 1, 10, u"", u"cm", u"", 0, u"", u"", u"", u"", u"")

#print f1.suggest(u"co", 10, 0)

#f1.add_ranking(u"ranking for 'license'", u"license", 44, 1, 0)
#f1.add_ranking(u"ranking for 'license' 2", u"license", 47, 5, 0)
f1.search(u"license", 1, 10, u"", u"cm", u"file", 0, u"", u"", u"", u"", u"")

#f1.remove_ranking(u"ranking for 'license'", u"license")
#f1.remove_ranking(u"ranking for 'license' 2", u"license")
f1.search(u"license", 1, 10, u"", u"cm", u"file", 0, u"", u"", u"", u"", u"")

print os.path.dirname(os.path.realpath(__file__))

f1.close()
f1.delete()