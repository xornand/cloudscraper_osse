from django.db import models
from django.utils.translation import ugettext_lazy as _ 
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from cores.models import Schedule
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import cores
from locals.utils import crawl_global, BrowseDirField

import logging
logger = logging.getLogger(__name__)

@python_2_unicode_compatible
class Directory(models.Model):

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    #start_dir = models.CharField(_('start_dir'), max_length=255)
    start_dir = BrowseDirField(_('start_dir'), max_length=255)
    recursive = models.BooleanField(_('recursive'), default=False)
    owner = models.ForeignKey(User, verbose_name=_('owner'))
    last_crawled_date = models.DateTimeField(_('last crawled date'), blank=True, null=True)
    status = models.CharField(_('status'), max_length=63, default='ready')
    schedule = models.ForeignKey(Schedule, verbose_name=_('schedule'))
    users = models.ManyToManyField(
        User,
        verbose_name=_('users'),
        blank=True,
        help_text=_(
            'The list of users allowed to search contents of this directory.'
            'If you leave chosen users empty, all users will be allowed to search.'
            'If you specify users, only these users will be allowed to search.'
        ),
        related_name="user_set",
        related_query_name="user"
    ) 
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Directory')
        verbose_name_plural = _('Directories')

@receiver(post_save, sender=Directory)
def post_save_callback(sender, instance, *args, **kwargs):

    # do not run callback when loading from fixture (manage.py loaddata)
    if kwargs.get('raw', False):
        return False
    
    # TODO: implement combinations of days, hours...
    if instance.schedule.type == "Interval":
        if instance.schedule.interval_days is not None:
            cores.sched.add_interval_job(
                crawl_global,
                days=instance.schedule.interval_days,
                args=[instance],
                name='Crawling dir ' + instance.title
            )
        elif instance.schedule.interval_minutes is not None:
            cores.sched.add_interval_job(
                crawl_global,
                minutes=instance.schedule.interval_minutes,
                args=[instance],
                name='Crawling dir ' + instance.title
            )
        elif instance.schedule.interval_seconds is not None:
            cores.sched.add_interval_job(
                crawl_global,
                seconds=instance.schedule.interval_seconds,
                args=[instance],
                name='Crawling dir ' + instance.title
            )
        else:
            logger.warn("Not implemented")
    
    elif instance.schedule.type == "Manual":
        logger.info("Scheduled manually")
    else:
        logger.warn("Not implemented")
    
    cores.sched.print_jobs()
    
    logger.info("Directory added/updated!")
    
    # test - get modeladmin instance
    from django.contrib import admin
    print admin.site._registry
    if sender in admin.site._registry:
        print admin.site._registry[sender]
    

@receiver(post_delete, sender=Directory)
def post_delete_callback(sender, instance, *args, **kwargs):
    
    jobs = cores.sched.get_jobs()
    job = None
    name = 'Crawling dir ' + instance.title
    for curjob in jobs:
        if curjob.name == name:
            job = curjob
    
    if job is not None:
        cores.sched.unschedule_job(job)
        logger.info('Job deleted successfully')
    else:
        logger.warn('Unable to delete job')


