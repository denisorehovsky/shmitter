from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tweet(models.Model):
    body = models.CharField(max_length=140, verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        verbose_name = _('tweet')
        verbose_name_plural = _('tweets')
        ordering = ['-created', ]
