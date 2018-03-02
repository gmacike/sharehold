from django.db import models

from catalogue.models import Commodity, BoardGameCommodity


class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=120)


class BoardGameContainer(models.Model):
    warehouse = models.ForeignKey(Warehouse)
    commodity = models.ForeignKey(BoardGameCommodity)
    total = models.IntegerField()

    class Meta:
        unique_together = ('warehouse', 'commodity')
