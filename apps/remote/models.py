from django.db import models
from django.utils.translation import ugettext_lazy as _ 
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from cores.models import Schedule
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import cores

import logging
logger = logging.getLogger(__name__)

@python_2_unicode_compatible
class Node(models.Model):

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    hostname = models.CharField(_('hostname'), max_length=255)
    port = models.IntegerField(_('port'), default=0)
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
        related_name="user_set_r",
        related_query_name="user_r"
    ) 
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')
