from django.db import models

from catalogue.models import Commodity, BoardGameCommodity


class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class BoardGameContainer(models.Model):
    warehouse = models.ForeignKey(Warehouse)
    commodity = models.ForeignKey(BoardGameCommodity)
    total = models.IntegerField()

    @property
    def available(self):
        return self.total - self.clienthasboardgame_set.count()

    class Meta:
        unique_together = ('warehouse', 'commodity')
