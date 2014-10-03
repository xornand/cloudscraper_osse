from django.db import models
from django.utils.translation import ugettext_lazy as _ 
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

@python_2_unicode_compatible
class Core(models.Model):

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    path = models.CharField(_('path'), default=settings.BASE_DIR + r"\apps\cores\cores", max_length=255)
    status = models.CharField(_('status'), max_length=63, default='ok')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Core')
        verbose_name_plural = _('Cores')

@python_2_unicode_compatible
class Schedule(models.Model):

    SCHEDULE_TYPE_CHOICES = (
        ('Cron', 'Cron'),
        ('Date', 'Date'),
        ('Interval', 'Interval'),
        ('Manual', 'Manual'),
    )

    title = models.CharField(_('title'), max_length=255)
    type = models.CharField(_('type'), max_length=15, choices=SCHEDULE_TYPE_CHOICES, default='Manual')
    cron_day = models.CharField(_('cron_day'), max_length=15, null=True)
    cron_month = models.CharField(_('cron_month'), max_length=15, null=True)
    cron_year = models.CharField(_('cron_year'), max_length=15, null=True)
    cron_hour = models.CharField(_('cron_hour'), max_length=15, null=True)
    cron_minute = models.CharField(_('cron_minute'), max_length=15, null=True)
    cron_second = models.CharField(_('cron_second'), max_length=15, null=True)
    cron_week = models.CharField(_('cron_week'), max_length=15, null=True)
    cron_day_of_week = models.CharField(_('cron_day_of_week'), max_length=15, null=True)
    cron_start_date = models.CharField(_('cron_start_date'), max_length=15, null=True)
    cron_end_date = models.CharField(_('cron_end_date'), max_length=15, null=True)
    cron_timezone = models.CharField(_('cron_timezone'), max_length=15, null=True)
    date_run_date = models.CharField(_('date_run_date'), max_length=31, null=True)
    date_timezone = models.CharField(_('date_timezone'), max_length=15, null=True)
    interval_weeks = models.IntegerField(_('interval_weeks'), null=True)
    interval_days = models.IntegerField(_('interval_days'), null=True)
    interval_hours = models.IntegerField(_('interval_hours'), null=True)
    interval_minutes = models.IntegerField(_('interval_minutes'), null=True)
    interval_seconds = models.IntegerField(_('interval_seconds'), null=True)
    interval_start_date = models.CharField(_('interval_start_date'), max_length=15, null=True)
    interval_end_date = models.CharField(_('interval_end_date'), max_length=15, null=True)
    interval_timezone = models.CharField(_('interval_timezone'), max_length=15, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')

@python_2_unicode_compatible
class Ranking(models.Model):

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    query = models.CharField(_('query'), max_length=255)
    docid = models.IntegerField(_('docid'), null=False)
    resno = models.IntegerField(_('resno'), null=False)
    # add for which user/users

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Ranking')
        verbose_name_plural = _('Rankings')

@python_2_unicode_compatible
class ContentDescriptor(models.Model):

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    mime_type = models.CharField(_('mime_type'), max_length=255)
    suffix = models.CharField(_('suffix'), max_length=31)
    magic_number = models.CharField(_('magic_number'), max_length=7, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Content descriptor')
        verbose_name_plural = _('Content descriptors')

@python_2_unicode_compatible
class Content(models.Model):

    CONTENT_TYPE_CHOICES = (
        ('File', 'File'),
        ('Email', 'Email'),
        ('Webpage', 'Webpage'),
        ('Other', 'Other'),
    )

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    type = models.CharField(_('type'), max_length=15, choices=CONTENT_TYPE_CHOICES, default='File')
    descriptor = models.ForeignKey(ContentDescriptor)
    # add for which user/users

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')

@python_2_unicode_compatible
class Filter(models.Model):

    FILTER_TYPE_CHOICES = (
        ('Descriptor', 'Descriptor'),
        ('Size', 'Size'),
        ('DateCreated', 'DateCreated'),
        ('DateModified', 'DateModified'),
    )

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    type = models.CharField(_('type'), max_length=15, choices=FILTER_TYPE_CHOICES, default='Descriptor')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')
