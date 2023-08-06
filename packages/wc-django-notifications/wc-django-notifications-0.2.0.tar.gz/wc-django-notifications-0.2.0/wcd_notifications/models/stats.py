from typing import Sequence
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import pgettext_lazy
from django.db import models
from django.contrib.postgres.indexes import BTreeIndex

from ..utils import make_generic_Q, ModelDef
from ..compat import JSONField


__all__ = 'StatsQuerySet', 'Stats',


class StatsQuerySet(models.QuerySet):
    def recipients(self, recipients: Sequence[ModelDef]):
        return self.filter(make_generic_Q('recipient', recipients))


class Stats(models.Model):
    objects = StatsQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy('wcd_notifications', 'Notification stats')
        verbose_name_plural = pgettext_lazy(
            'wcd_notifications', 'List of notifications stats'
        )
        ordering = ('-pk',)
        indexes = [
            BTreeIndex(fields=['recipient_content_type', 'recipient_object_id']),
        ]

    recipient_content_type = models.ForeignKey(
        ContentType,
        verbose_name=pgettext_lazy('wcd_notifications', 'Recipient: Content type'),
        related_name='stats_recipient', on_delete=models.CASCADE,
    )
    recipient_object_id = models.CharField(
        verbose_name=pgettext_lazy('wcd_notifications', 'Recipient: Id'),
        max_length=255, null=False, blank=False,
    )
    recipient = GenericForeignKey('recipient_content_type', 'recipient_object_id')
    flags = JSONField(
        verbose_name=pgettext_lazy('wcd_notifications', 'Flags stats'),
        blank=True, null=False, default=dict,
    )
    total = models.BigIntegerField(
        verbose_name=pgettext_lazy('wcd_notifications', 'Total'),
        default=0,
    )

    def __str__(self):
        return str(self.pk)
