from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.urls import reverse
from warehouse.models import BoardGameContainer


class Customer(models.Model):
    registrationNumber = models.IntegerField(unique=True)
    initials = models.CharField(max_length=10)

    def active_IDs_count (self):
        return self.customerIDs.filter(IDstatus=CustomerID.AKTYWNY).count()

    def __str__(self):
        return '{} {}'.format(self.initials, self.registrationNumber)

    def get_absolute_url(self):
        return reverse('circulation_customeredit', kwargs={'pk': self.pk})

    def get_unfinished_lendings_count(self):
        return BoardGameLending.objects.filter(customer=self, returned=None).count()

class CustomerID(models.Model):
    customer = models.ForeignKey('Customer',
                                     on_delete=models.CASCADE,
                                     related_name='customerIDs',
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

    @classmethod
    def create(cls, cust, label):
        customerID = cls(customer=cust, IDlabel=label)
        customerID.activate()
        return customerID

    def activate (self):
        # only allow to activate ID if customer is allowed to have additional active one otherwise raise a model ValidationError
        other_active_IDs_count = self.customer.customerIDs.exclude(pk=self.pk).filter(IDstatus=CustomerID.AKTYWNY).count()
        if other_active_IDs_count < settings.CIRCULATION_MAX_ACTIVE_IDS:
            if self.IDstatus == CustomerID.AKTYWNY:
                pass
            elif self.IDstatus == CustomerID.ZABLOKOWANY:
                self.IDstatus = CustomerID.AKTYWNY
            else:
                raise ValidationError ('Identyfikator nie może zostać aktywowany', code='CustomerID state machine violated')
        else:
            raise ValidationError ('Dla klienta nie może być aktywowany kolejny identyfikator', code='too many active ')

    def deactivate (self):
        # only allow active ID to be deactivated otherwise raise a model ValidationError
        if self.IDstatus == CustomerID.AKTYWNY:
            self.IDstatus = CustomerID.ZABLOKOWANY
        elif self.IDstatus == CustomerID.ZABLOKOWANY:
            pass
        else:
            raise ValidationError ('Identyfikator nie jest aktywny', code='CustomerID state machine violated')

    def get_status_str (self):
        status_desc = None
        for status in CustomerID.CustomerID_STATUS:
            if status [0] == self.IDstatus:
                status_desc = status [1]
                break
        return status_desc

    def active (self):
        return self.IDstatus == CustomerID.AKTYWNY

    # def save(self, *args, **kwargs):
    #     do_something()
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
    #     do_something_else()


    def __str__(self):
        return '{}@{}:{}'.format(self.IDlabel, self.customer, CustomerID.CustomerID_STATUS[self.IDstatus])


class BoardGameLending(models.Model):
    customer = models.ForeignKey(Customer,
                                     on_delete=models.CASCADE,
                                     related_name='lendings',
                                     null=False,
                                     blank=False)
    # customerID = models.ForeignKey(CustomerID,
    #                                  on_delete=models.CASCADE,
    #                                  related_name='lendings',
    #                                  null=False,
    #                                  blank=False)
    container = models.ForeignKey(BoardGameContainer,
                                     on_delete=models.CASCADE,
                                     related_name='lendings',
                                     null=False,
                                     blank=False)


    issued = models.DateTimeField(null=False, default=timezone.now)
    returned = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        # count customer's lendings and check if limit will not be exceeded
        qs = BoardGameLending.objects.filter(customer=self.customer)
        unfinished_customer_lendings_cnt = qs.count()
        if unfinished_customer_lendings_cnt >= settings.CIRCULATION_MAX_LENDINGS_PER_CUSTOMER:
            raise ValidationError ('Klient wyczerpał limit {} wypożyczeń, ma ich: {}'.format(settings.CIRCULATION_MAX_LENDINGS_PER_CUSTOMER, self.customer.get_unfinished_lendings_count()), 'model constraint violation')

        #check if limit per customerID won't be exceeded
        # unfinished_customerID_lendings_cnt = qs.filter (customerID=self.customerID).count()
        # if unfinished_customerID_lendings_cnt >= settings.CIRCULATION_MAX_LENDINGS_PER_CUSTOMERID:
        #     raise ValidationError ('Dla identyfikatora wyczerpano limit wypożyczeń', 'model constraint violation')

        #start lending from now on
        self.issued = timezone.now()

        # TODO: add following to MIDDLEWARE - https://docs.djangoproject.com/en/2.0/topics/i18n/timezones/
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} <-> {} from {}, to'.format (self.customer, self.container, self.issued, self.returned)
