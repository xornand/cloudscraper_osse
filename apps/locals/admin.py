from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.utils import timezone
import cores

from locals.utils import crawl_global

import logging
logger = logging.getLogger(__name__)

class DirectoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_crawled_date'
    list_display = ('title', 'start_dir', 'last_crawled_date', 'status',)
    list_filter = ('title', 'start_dir', 'last_crawled_date',)
    search_fields = ('title',)
    actions = ['crawl']
    list_per_page = 10
    fieldsets = (
        ('', {
            'fields': ('title', 'start_dir', 'recursive'),
        }),
        (capfirst(_('description')), {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        (capfirst(_('owner')), {
            'fields': ('owner',),
            'classes': ('collapse collapse-opened',),
        }),
        (capfirst(_('schedule')), {
            'fields': ('schedule',),
            'classes': ('collapse collapse-opened',),
        }),
        (capfirst(_('permissions')), {
            'fields': ('users',),
            'classes': ('collapse collapse-opened',),
        }), 
    )
    filter_horizontal = ('users',)
    
    def crawl(self, request, queryset):
    
        from datetime import datetime, timedelta
        trigger_time = datetime.now() + timedelta(seconds=1)
    
        for curmodel in queryset:
            cores.sched.add_date_job(crawl_global, trigger_time, name='Crawling dir ' + curmodel.title, jobstore='default', args=[curmodel]) 
            queryset.update(status='running', last_crawled_date=timezone.now())
        
        cores.sched.print_jobs()
    
    crawl.short_description = "Crawl selected directories now"


