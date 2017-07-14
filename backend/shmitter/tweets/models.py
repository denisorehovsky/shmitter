from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tweet(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='tweets', verbose_name=_('owner'))
    body = models.CharField(max_length=140, verbose_name=_('body'))
    likes = GenericRelation('likes.Like')
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        verbose_name = _('tweet')
        verbose_name_plural = _('tweets')
        ordering = ['-created', ]

    def __str__(self):
        return 'Tweet {}'.format(self.id)

    @property
    def total_likes(self):
        return self.likes.count()
