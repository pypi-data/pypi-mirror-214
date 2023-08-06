from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from django.urls import reverse

class Keycard(NetBoxModel):
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='keycard'
    )
    cardnumber = models.IntegerField()
    firstname = models.TextField(
        max_length=50
    )
    lastname = models.TextField(
        max_length=50
    )

    class Meta:
        ordering = ('cardnumber',)

    def __str__(self):
        return str(self.cardnumber)

    def get_absolute_url(self):
        return reverse('plugins:netbox_sb_dc_accessdata:keycard', args=[self.pk])


class Key(NetBoxModel):
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='key'
    )
    keynumber = models.TextField(
        max_length=10
    )
    firstname = models.TextField(
        max_length=50
    )
    lastname = models.TextField(
        max_length=50
    )

    class Meta:
        ordering = ('keynumber',)

    def __str__(self):
        return str(self.keynumber)

    def get_absolute_url(self):
        return reverse('plugins:netbox_sb_dc_accessdata:key', args=[self.pk])



