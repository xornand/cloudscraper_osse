import logging

from django.conf import settings
from django.contrib import admin

from django_mailbox.models import MessageAttachment, Message, Mailbox
from django_mailbox.signals import message_received
from django_mailbox.utils import convert_header_to_unicode

from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from django_mailbox.utils import crawl_global
import cores
from django.utils import timezone

logger = logging.getLogger(__name__)


# def get_new_mail(mailbox_admin, request, queryset):
    # for mailbox in queryset.all():
        # logger.debug('Receiving mail for %s' % mailbox)
        # mailbox.get_new_mail()
# get_new_mail.short_description = 'Get new mail'

def resend_message_received_signal(message_admin, request, queryset):
    for message in queryset.all():
        logger.debug('Resending \'message_received\' signal for %s' % message)
        message_received.send(sender=message_admin, message=message)
resend_message_received_signal.short_description = (
    'Re-send message received signal'
)


class MailboxAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        #'uri',
        #'from_email',
        'description',
        #'active',
        'last_crawled_date',
        'status',
    )
    fieldsets = (
        ('', {
            'fields': ('name', 'uri'),
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
    #actions = [get_new_mail]
    actions = ['crawl']
    filter_horizontal = ('users',)
    
    def crawl(self, request, queryset):
    
        from datetime import datetime, timedelta
        trigger_time = datetime.now() + timedelta(seconds=1)
    
        for curmodel in queryset:
            cores.sched.add_date_job(crawl_global, trigger_time, name='Crawling mailbox ' + curmodel.name, jobstore='default', args=[curmodel]) 
            queryset.update(status='running', last_crawled_date=timezone.now())
        
        cores.sched.print_jobs()
    
    crawl.short_description = "Crawl selected mailboxes now"


class MessageAttachmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('message', )
    list_display = ('message', 'document',)


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    def attachment_count(self, msg):
        return msg.attachments.count()

    def subject(self, msg):
        return convert_header_to_unicode(msg.subject)

    inlines = [
        MessageAttachmentInline,
    ]
    list_display = (
        'subject',
        'processed',
        'read',
        'mailbox',
        'outgoing',
        'attachment_count',
    )
    ordering = ['-processed']
    list_filter = (
        'mailbox',
        'outgoing',
        'processed',
        'read',
    )
    exclude = (
        'body',
    )
    raw_id_fields = (
        'in_reply_to',
    )
    readonly_fields = (
        'text',
    )
    actions = [resend_message_received_signal]

if getattr(settings, 'DJANGO_MAILBOX_ADMIN_ENABLED', True):
    admin.site.register(Message, MessageAdmin)
    admin.site.register(MessageAttachment, MessageAttachmentAdmin)
    admin.site.register(Mailbox, MailboxAdmin)
