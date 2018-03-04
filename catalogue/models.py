# from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

# Create your models here.

#abstract class for commodities to be catalogued
class Commodity (models.Model):
    catalogueEntry = models.ForeignKey ('CatalogueItem',
        on_delete=models.CASCADE, related_name='commodities', null=True, blank=False)

    BARCODE = 'BAR'
    QRCODE = 'QR'
    CODE_TYPES = (
        (BARCODE, 'Barcode'),
        (QRCODE, 'QR code'),
    )

    codeType = models.CharField (
        max_length = 3,
        choices = CODE_TYPES,
        default = BARCODE,
    )

    codeValue = models.CharField (
        max_length = 20,
        null = True,
        unique = True,
        verbose_name = "Etykieta kodu"
    )

    class Meta:
        abstract = True

    def codeValueToStr (self):
        if self.codeType == Commodity.BARCODE:
            return self.codeValue


class BoardGameCommodity (Commodity):
    catalogueEntry = models.ForeignKey ('BoardGameItem',
        on_delete=models.CASCADE, related_name='commodities', null=True, blank=False)

    description = models.TextField (
        verbose_name = 'Informacje o wydaniu',
        max_length = 300,
        blank = True,
        null = True,
    )


    boxFrontImage = models.ImageField (upload_to="bg/img/", null = True, blank=True)
    boxTopImage = models.ImageField (upload_to="bg/img/", null = True, blank=True)
    boxSideImage = models.ImageField (upload_to="bg/img/", null = True, blank=True)

    class Meta:
        verbose_name = "Wydanie gry planszowej"

    # def __init__(self, entry):
    #     super().__init__()
    #     self.catalogueEntry = entry

    def __str__(self):
        return self.catalogueEntry.__str__()+": "+self.codeValueToStr()

    def get_absolute_url(self):
        return reverse("catalogue_entries")

    # def getBoxImageURL(self, boxImage):
    #     return boxImage


#abstract class for univeral handling catalogued items
class CatalogueItem (models.Model):
    itemLabel = models.CharField (max_length = 50)

    class Meta:
        abstract = True
        ordering = ['itemLabel']

    def __str__ (self):
        return self.itemLabel

    def getCommodities (self):
        return None


class BoardGameItem (CatalogueItem):
    bggURL = models.URLField (
        max_length = 100,
        blank = True)
    baseGameItem = models.ForeignKey (
        'catalogue.BoardGameItem',
        related_name = 'extensions',
        related_query_name="basegame",
        null = True,
        blank = True)

    def getTitle (self):
        return self.itemLabel

    def setTitle (self, title):
        self.itemLabel = title

    def get_absolute_url(self):
        return reverse("catalogue_entries")

    def getCommodities (self):
        return self.commodities
