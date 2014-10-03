import os
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User, Group
from django.conf import settings

import cores

from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_str

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group

class SearchViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def list(self, request, format=None):
    
        params = request.QUERY_PARAMS
        
        # print params
        
        q = params.get('q', u'')
        start = params.get('start', 1)
        hitsPerPage = params.get('hitsPerPage', 10)
        sort = params.get('sort', u'')
        order = params.get('order', u'')
        mode = params.get('mode', u'cm')
        facet = params.get('facet', u'')
        uid = params.get('uid', 0)
        df = params.get('df', u'')
        dfFrom = params.get('df.from', u'')
        dfTo = params.get('df.to', u'')
        lf = params.get('lf', u'')
        lfl = params.get('lf.l', u'')
        ff = params.get('ff', u'')
        ffct = params.get('ff.ct', u'')
        
        #res = cores.f1.search(q, int(start), int(hitsPerPage), sort, order, mode, facet, int(uid), u"", u"", u"", u"", u"")
        res = cores.f1.search(q, int(start), int(hitsPerPage), sort, order, mode, facet, int(uid), df, dfFrom, dfTo, lf, lfl, ff, ffct)
        #print type(res)
        
        #sys.stdout.write(buf.value.encode("utf-8") + "\n")
        #resd = res.decode("utf-16-le")
        #res = "<?xml version='1.0'?><root/>"
        
        return Response(res, status=status.HTTP_200_OK)

class SuggestViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def list(self, request, format=None):
    
        params = request.QUERY_PARAMS
        
        # print params
        
        q = params.get('q', u'')
        n = params.get('n', 10)
        uid = params.get('uid', 0)
        
        res = cores.f1.suggest(q, int(n), int(uid))
        
        return Response(res, status=status.HTTP_200_OK)

class UploadViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def list(self, request, format=None):
    
        params = request.QUERY_PARAMS
        
        # print params
        
        
        
        return Response("OK", status=status.HTTP_200_OK)

class DownloadViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def list(self, request, format=None):
    
        params = request.QUERY_PARAMS
        
        # print params
        path = params.get('path', u'')
        name = params.get('name', u'')
        ctype = params.get('content_type', u'')
        download = params.get('download', u'true')  # default is true
        
        #response = HttpResponseRedirect('/media/locals/127.0.0.1' + path + '/' + name) 
        #response['Content-Type'] = content_type
        #response['Content-Disposition'] = "attachment; filename='" + name + "'"
        
        #path_to_file = "/media/locals/127.0.0.1{0}".format(path)
        #response = HttpResponse(mimetype='application/force-download')
        #response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(name)
        #response['X-Sendfile'] = smart_str(path_to_file)
        
        if (download == "true"):
        
            # based on https://djangosnippets.org/snippets/365/ and
            # http://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
            # we do not use /media nor xsendfile (not sure how to add xsendfile into dev server)
            
            # you can use this as well https://django-downloadview.readthedocs.org/en/1.6/index.html
            
            # WARNING: HttpResponse is deprecated!
            
            filename = os.path.join(settings.BASE_DIR, "apps", "cores", "incoming\\locals\\127.0.0.1{0}".format(path), name) # Select your file here.                                
            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper, content_type=ctype)
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(name)
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Transfer-Encoding'] = 'binary';
            
            return response
        
        else:
            
            #open file using /media
            return HttpResponseRedirect('/media/locals/127.0.0.1' + path + '/' + name)

class BrowseViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def list(self, request, format=None):
    
        params = request.QUERY_PARAMS
        
        # jstree will send id automatically
        id = params.get('id', u'')
        
        # json = [
           # { "id" : "1", "parent" : "#", "text" : "C:/Users/Bratislav/Downloads/tests1"},
           # { "id" : "2", "parent" : "#", "text" : "C:/Users/Bratislav/Downloads/tests2"},
           # { "id" : "3", "parent" : "2", "text" : "C:/Users/Bratislav/Downloads/tests2/abc" },
           # { "id" : "4", "parent" : "2", "text" : "C:/Users/Bratislav/Downloads/tests2/def" },
        # ]
        
        startdir = ""
        # jstree will send # for root nodes
        if id == "#":
            startdir = settings.BROWSE_STARTDIR
        else:
            startdir = os.path.join(settings.BROWSE_STARTDIR, id)
        
        print "id is %s" % id
        print "startdir is %s" % startdir
        
        subdirs = [name for name in os.listdir(startdir) if os.path.isdir(os.path.join(startdir, name))]
        json = []
        # do not use integers as ids!!! If you have multiple nodes with the same id, jstree will
        # behave unexpectedly!!!
        for dir in subdirs:
            json.append({ "id" : os.path.join(startdir, dir), "text" : dir, "children" : True })
        
        return Response(json, status=status.HTTP_200_OK)