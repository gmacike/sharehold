from django.db import models

from catalogue.models import BoardGameItem


class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=120)


class Container(models.Model):
    warehouse = models.ForeignKey(Warehouse)
    board_game = models.ForeignKey(BoardGameItem)
    total = models.IntegerField()

    class Meta:
        unique_together = ('warehouse', 'board_game')
