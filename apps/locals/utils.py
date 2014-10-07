from shutil import copytree, ignore_patterns, rmtree
from django.conf import settings
import os
import cores

from ctypes import *

from django.forms import widgets
from django.db import models
from django.utils.safestring import mark_safe

import logging
logger = logging.getLogger(__name__)

def crawl_global(curmodel):

    logger.info("Crawling %s started" % curmodel.title)
        
    # copy from start_dir into incoming/locals/localhost so /media can server it for download
    start_dir_fixed = curmodel.start_dir.replace(":", "")
    dst = os.path.join(settings.BASE_DIR, 'apps', 'cores', 'incoming', 'locals', '127.0.0.1', start_dir_fixed)
    
    # delete dst first, because copytree will complain if it already exists
    rmtree(dst, ignore_errors=True)
    logger.info("Incoming dir %s cleared successfully" % dst)
    
    
    # check to see if we need to do this recursively
    #ignore = None
    #if curmodel.recursive:
        #ignore = lambda : [name for name in os.listdir(curmodel.start_dir) if os.path.isdir(os.path.join(curmodel.start_dir, name))]
    
    ext_to_filter = ['.'+desc.suffix for filter in curmodel.filters.all() for content in filter.contents.all() for desc in content.descriptors.all()]
    
    # this will get called when copytree starts processing dir (or subdir)
    # path is the current dir and names are contents (both dirs and files) in that dir
    def custom_ignore_patterns(dir):
        def _ignore_patterns(path, names):
            
            #print 'filters: %s' % ext_to_filter
            #print 'path %s' % path
            #print 'names %s' % names
            
            logger.info("Copying %s..." % path)
            
            if not curmodel.recursive:
                # filter both subdirs and filenames that match filters
                ignored_names = [name for name in names if os.path.isdir(os.path.join(path, name))]
                ignored_names = [name for name in names if not name.endswith(tuple(ext_to_filter))]
            else:
                # filter only filenames that match filters
                #print 'listdir %s' % os.listdir(dir)
                ignored_names = [name for name in names if not os.path.isdir(os.path.join(path, name)) and not name.endswith(tuple(ext_to_filter))]
            #print 'Ignored %s' % set(ignored_names)
            return set(ignored_names)
        return _ignore_patterns
    
    #copytree(curmodel.start_dir, dst, ignore=ignore_patterns('*.pyc', 'tmp*'))
    #if curmodel.recursive:
        #copytree(curmodel.start_dir, dst, ignore=None)
    #else:
        ## ignore (filter) subdirs
        #copytree(curmodel.start_dir, dst, ignore=custom_ignore_patterns(curmodel.start_dir))
    
    copytree(curmodel.start_dir, dst, ignore=custom_ignore_patterns(curmodel.start_dir))
    
    logger.info("Files copied into incoming dir %s successfully" % dst)
    
    #queryset.update(status='running', last_crawled_date=timezone.now())
    
    nusers = curmodel.users.count()
    print "Num of users is %d" % nusers
    
    # index start_dir, not dst (incoming subfolder) because path_s needs to be set correctly!
    #cores.f1.index("127.0.0.1", "8000", curmodel.start_dir, "file", 0)
    #uidsArray = (c_int * 2)()
    
    # if nusers == 0, we add one uid (uid == 0)
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
    
    #cores.f1.index("127.0.0.1", "8000", curmodel.start_dir, "file", uidsArray, len(uidsArray))
    cores.f1.index("127.0.0.1", "8000", dst, "file", uidsArray, len(uidsArray), curmodel.start_dir)
    
    cores.f1.commit()
    
    logger.info("Crawling %s completed successfully" % curmodel.title)

# custom widget and field for directory
class BrowseDirWidget(widgets.TextInput):

    def render(self, name, value, attrs=None):
        
        html = super(BrowseDirWidget, self).render(name, value, attrs)
        
        html = """
        <link rel="stylesheet" href="/static/jstree/themes/default/style.min.css" />
        <!-- 4 include the jQuery library -->
        <script src="/static/jstree/libs/jquery.js"></script>
        <!-- 5 include the minified jstree source -->
        <script src="/static/jstree/jstree.min.js"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
        
        <script type="text/javascript">
            var showBrowseDialog = function() {
                // Use jQuery to select the fields that will
                // populate this field
                $('#jstree').jstree({
                        "plugins" : ["wholerow", "checkbox"],
                        "core" : {
                            "data" : {
                                "url" : "http://""" + settings.SEARCH_PAGE_HOSTNAME + """:""" + settings.SEARCH_PAGE_PORT + """/api/browse?format=json",
                                "data" : function(node) {
                                    return {
                                        'id' : node.id
                                    };
                                }
                            },
                            "multiple" : false,
                        }
                    });
                // 7 bind to events triggered on the tree
                $('#jstree').on("changed.jstree", function (e, data) {
                  console.log(data.selected);
                });
                
                // create dialog
                $('#dialog').dialog({
                            modal: true,
                            resizable: true,
                            width: 650,
                            height: 400,
                            buttons: {
                                "Select": function() {
                                    // set value of text input
                                    console.log('getting checked directory...');
                                    var id = $("#jstree").jstree('get_checked');
                                    console.log('setting value...');
                                    if (id) {
                                        $('#id_start_dir').val(id);
                                    }
                                    $( this ).dialog( "close" );
                                },
                                "Cancel": function() {
                                  $( this ).dialog( "close" );
                                },
                              }
                        });
            } 
        </script>
        """ + html + """
        <button id="browseDirBtn" type="button" onclick="showBrowseDialog()">
            Browse
        </button>
        <div id="dialog" title="Browse">
            <div id="jstree">
            </div>
        </div>
        """;
            
        # Since we are using string concatenation, we need to
        # mark it as safe in order for it to be treated as
        # html code.
        return mark_safe(html);

class BrowseDirField(models.CharField):

    def formfield(self, **kwargs):
        kwargs['widget'] = BrowseDirWidget
        return super(BrowseDirField, self).formfield(**kwargs)