from django.db import models
from django.db.models import Sum
from django.apps import apps
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from warehouse.models import BoardGameContainer

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

    def get_commodity_by_code (self, code_type, code_value):
        return None


class BoardGameCommodity (Commodity):
    catalogueEntry = models.ForeignKey ('BoardGameItem',
        on_delete=models.CASCADE, related_name='commodities', null=True, blank=False)

    description = models.TextField (
        verbose_name = 'Informacje o wydaniu',
        max_length = 300,
        blank = True,
        null = True,
    )


    boxFrontImage = models.ImageField (upload_to="catalogue/bg/%M", null = True, blank=True)
    boxTopImage = models.ImageField (upload_to="catalogue/bg/%M", null = True, blank=True)
    boxSideImage = models.ImageField (upload_to="catalogue/bg/%M", null = True, blank=True)

    class Meta:
        verbose_name = "Wydanie gry planszowej"

    # def __init__(self, entry):
    #     super().__init__()
    #     self.catalogueEntry = entry

    def __str__(self):
        return self.catalogueEntry.__str__()+": "+self.codeValueToStr()

    def get_absolute_url(self):
        return reverse("catalogue_entries")

    def get_commodity_by_code (code_type, code_value):
        return BoardGameCommodity.objects.filter (codeValue=code_value).filter (codeType=code_type)

    def getImage(self):
        image = None
        if self.boxFrontImage:
            image = self.boxFrontImage
        elif self.catalogueEntry.itemImage:
            image = self.catalogueEntry.itemImage
        return image    


#abstract class for univeral handling catalogued items
class CatalogueItem (models.Model):
    itemLabel = models.CharField (max_length = 50)
    # keeping all media files in one folder is not efficient, override this in subclasses
    itemImage = models.ImageField (upload_to="catalogue/", null = True, blank=True)


    class Meta:
        abstract = True
        ordering = ['itemLabel']

    def __str__ (self):
        return self.itemLabel

    def getCommodities (self):
        return None

    def getImage(self):
        return self.itemImage

    def commoditiesTotalCount(self):
        return Commodity.objects.none();

    def commoditiesAvailableCount(self):
        return 0;


class BoardGameItem (CatalogueItem):
    itemImage = models.ImageField (upload_to="catalogue/bg/", null = True, blank=True)

    bggURL = models.URLField (
        max_length = 100,
        null = True,
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

    def getImage(self):
        image = None
        if self.itemImage:
            image = self.itemImage
        else:
            # search for commodities w/ front image
            commodities = self.commodities.exclude(boxFrontImage="")
            if commodities.exists():
                for commodity in commodities:
                    if bool(commodity.boxFrontImage):
                        image = commodity.boxFrontImage
                        break
        return image

    def commoditiesTotalCount(self):
        agg = BoardGameContainer.objects.filter(commodity__catalogueEntry=self).aggregate(total=Sum('total'))
        total = agg ['total']
        if total == None:
            return 0
        return total


    def commoditiesAvailableCount(self):
        available = 0
        containers = BoardGameContainer.objects.filter(commodity__catalogueEntry=self)
        if containers.exists():
            for container in containers:
                available += container.available
        return available
