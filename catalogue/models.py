from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

# Create your models here.

#abstract class for univeral handling catalogued items
class CatalogueItem (models.Model):
    itemLabel = models.CharField (max_length = 50)

    class Meta:
        abstract = True

    def __str__ (self):
        return self.itemLabel

#abstract class for handling items with barcode, QRcode etc - any sort of outside identifier
class CodeLabelledItem (CatalogueItem):
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
        if self.codeType == CodeLabelledItem.BARCODE:
            return self.codeValue


class BoardGameItem (CodeLabelledItem):
    # frontImage = models.ImageField
    # sideImages = models.ImageField
    bggURL = models.URLField (
        max_length = 100,
        blank = True)
    basegame = models.ForeignKey (
        'catalogue.BoardGameItem',
        related_name = 'extensions',
        null = True)

    def getTitle (self):
        return self.itemLabel

    def setTitle (self, title):
        self.itemLabel = title

    def get_absolute_url(self):
        return reverse("catalogue_entries")

    def codeValueToStr (self):
        if self.codeType == CodeLabelledItem.BARCODE:
            return self.codeValue [0]+" "+ self.codeValue[1:6]+" "+ self.codeValue[7:12]


class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=120)


class Container(models.Model):
    warehouse = models.ForeignKey(Warehouse)
    board_game = models.ForeignKey(BoardGameItem)
    total = models.IntegerField()

    class Meta:
        unique_together = ('warehouse', 'board_game')
