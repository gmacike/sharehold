from datetime import datetime
from django.db import models

from warehouse.models import BoardGameContainer


class RentalClient(models.Model):
    registrationNumber = models.IntegerField(unique=True)
    initials = models.CharField(max_length=10)

    def __str__(self):
        return '{} {}'.format(self.initials, self.registrationNumber)


class ClientID(models.Model):
    rentalClient = models.ForeignKey('RentalClient',
                                     on_delete=models.CASCADE,
                                     related_name='clientIDs',
                                     null=True,
                                     blank=False)
    IDlabel = models.CharField(max_length=12, unique=True, verbose_name='Identyfikator')
    active = models.BooleanField(default=True, verbose_name='Aktywny')

    def __str__(self):
        return '{}@{}'.format(self.IDlabel, self.rentalClient)


class BoardGameLending(models.Model):
    client = models.ForeignKey(RentalClient)
    container = models.ForeignKey(BoardGameContainer)

    issued = models.DateTimeField(default=datetime.now)
    returned = models.DateTimeField(null=True)

    def __str__(self):
        return '{} <-> {} from {}, to'.format (self.client, self.container, self.issued, self.returned)
