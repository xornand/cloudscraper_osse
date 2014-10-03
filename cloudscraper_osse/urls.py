from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from .admin import admin, staff, user
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from rest_framework import routers

import cores

from cores.views import CustomSearchView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_str
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import os
from cloudscraper_osse.rest import UserViewSet, GroupViewSet, SearchViewSet, SuggestViewSet, UploadViewSet, DownloadViewSet, BrowseViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'search', SearchViewSet, r'search')
router.register(r'suggest', SuggestViewSet, r'suggest')
router.register(r'upload', UploadViewSet, r'upload')
router.register(r'download', DownloadViewSet, r'download')
router.register(r'browse', BrowseViewSet, r'browse')

urlpatterns = patterns(
    '',
    url(r'^adminpanel/', include(admin.urls)),
    url(r'^staffpanel/', include(staff.urls)),
    url(r'^userpanel/', include(user.urls)),
    #url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    #url(r'^search/', TemplateView.as_view(template_name='search.html')),
    url(r'^search/', CustomSearchView.as_view(), name='search_view'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/cores/images/favicon.ico')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
