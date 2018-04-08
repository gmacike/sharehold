from datetime import datetime
from django.db import models

from warehouse.models import BoardGameContainer


class RentalClient(models.Model):
    identificationCode = models.IntegerField(unique=True)
    initials = models.CharField(max_length=10)

    def __str__(self):
        return '{} {}'.format(self.initials, self.identificationCode)


class ClientID(models.Model):
    rentalClient = models.ForeignKey('RentalClient',
                                     on_delete=models.CASCADE,
                                     related_name='client',
                                     null=True,
                                     blank=False)
    ID = models.IntegerField(primary_key=True, unique=True, verbose_name='Identyfikator')
    active = models.BooleanField(default=True, verbose_name='Aktywny')


class ClientHasBoardGame(models.Model):
    client = models.ForeignKey(RentalClient)
    container = models.ForeignKey(BoardGameContainer)
    issued = models.DateTimeField(default=datetime.now)
    returned = models.DateTimeField(null=True)
