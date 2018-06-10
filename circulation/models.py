from datetime import datetime
from django.conf import settings
from django.db import models

from warehouse.models import BoardGameContainer


class Customer(models.Model):
    registrationNumber = models.IntegerField(unique=True)
    initials = models.CharField(max_length=10)

    def active_IDs_count (self):
        return self.CustomerIDs.filter(status=CustomerID.AKTYWNY).count()

    def __str__(self):
        return '{} {}'.format(self.initials, self.registrationNumber)


class CustomerID(models.Model):
    customer = models.ForeignKey('Customer',
                                     on_delete=models.CASCADE,
                                     related_name='CustomerIDs',
                                     null=False,
                                     blank=False)
    IDlabel = models.CharField(max_length=12, unique=True, null=False, blank=False, verbose_name='Identyfikator')

    AKTYWNY = 0
    ZABLOKOWANY = 1
    UTRACONY = 2
    ZWROCONY = 3
    CustomerID_STATUS = (
        (AKTYWNY, 'Aktywny'),
        (ZABLOKOWANY, 'Zablokowany'),
        (UTRACONY, 'Utracony'),
        (ZWROCONY, 'Zwrócony'),
    )

    IDstatus = models.IntegerField(default=AKTYWNY, verbose_name='Status identyfikatora')

    def activate (self):
        if self.customer.active_IDs_count < settings.CIRCULATION_MAX_ACTIVE_IDS:
            self.IDstatus = CustomerID.AKTYWNY
        else:
            raise CustomerID.StatusError

    def aktywny (self):
        return self.IDstatus == AKTYWNY

    def __str__(self):
        return '{}@{}'.format(self.IDlabel, self.customer)


class BoardGameLending(models.Model):
    customer = models.ForeignKey(Customer)
    container = models.ForeignKey(BoardGameContainer)

    issued = models.DateTimeField(default=datetime.now)
    returned = models.DateTimeField(null=True)

    def __str__(self):
        return '{} <-> {} from {}, to'.format (self.customer, self.container, self.issued, self.returned)
