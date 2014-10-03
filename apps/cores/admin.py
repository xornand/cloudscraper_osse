from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from djadmin_ext.helpers import BaseAjaxModelAdmin
from forms import ScheduleForm

class CoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'status',)
    list_filter = ('title', 'path', 'status',)
    search_fields = ('title','path',)
    list_per_page = 10
    fieldsets = (
        ('', {
            'fields': ('title', 'path'),
        }),
        (capfirst(_('description')), {
            'fields': ('description',),
            'classes': ('collapse collapse-opened',),
        }),
    )

class ScheduleAdmin(BaseAjaxModelAdmin):
    list_display = ('title', 'type',)
    list_filter = ('title', 'type',)
    search_fields = ('title',)
    list_per_page = 10
    form = ScheduleForm

class RankingAdmin(admin.ModelAdmin):
    list_display = ('title','docid', 'resno',)
    list_filter = ('title', 'query',)
    search_fields = ('title',)
    list_per_page = 10
    fieldsets = (
        ('', {
            'fields': ('title', 'query', 'docid', 'resno',),
        }),
        (capfirst(_('description')), {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
    )

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 10
    fieldsets = (
        ('', {
            'fields': ('title',),
        }),
        (capfirst(_('description')), {
            'fields': ('description',),
            'classes': ('collapse collapse-opened',),
        }),
    )

class ContentDescriptorAdmin(admin.ModelAdmin):
    list_display = ('title','suffix','mime_type')
    list_filter = ('title','mime_type')
    search_fields = ('title','mime_type','suffix',)
    list_per_page = 10
    fieldsets = (
        ('', {
            'fields': ('title','mime_type', 'suffix', 'magic_number'),
        }),
        (capfirst(_('description')), {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
    )

class FilterAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')
    list_filter = ('title','type')
    search_fields = ('title','type')
    list_per_page = 10
    fieldsets = (
        ('', {
            'fields': ('title','type',),
        }),
        (capfirst(_('description')), {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
    )
