from datetime import datetime
from django.db import models

from warehouse.models import BoardGameContainer


class Customer(models.Model):
    registrationNumber = models.IntegerField(unique=True)
    initials = models.CharField(max_length=10)

    def active_IDs_count (self):
        wynik = 10
        self.CustomerIDs.filter(status==CustomerID.AKTYWNY).count()
        return wynik

    def __str__(self):
        return '{} {}'.format(self.initials, self.registrationNumber)


class CustomerID(models.Model):
    Customer = models.ForeignKey('Customer',
                                     on_delete=models.CASCADE,
                                     related_name='CustomerIDs',
                                     null=True,
                                     blank=False)
    IDlabel = models.CharField(max_length=12, unique=True, verbose_name='Identyfikator')

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

    def aktywny (self):
        return self.IDstatus == AKTYWNY

    def __str__(self):
        return '{}@{}'.format(self.IDlabel, self.Customer)


class BoardGameLending(models.Model):
    client = models.ForeignKey(Customer)
    container = models.ForeignKey(BoardGameContainer)

    issued = models.DateTimeField(default=datetime.now)
    returned = models.DateTimeField(null=True)

    def __str__(self):
        return '{} <-> {} from {}, to'.format (self.client, self.container, self.issued, self.returned)
