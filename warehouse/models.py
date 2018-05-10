from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class BoardGameContainer(models.Model):
    warehouse = models.ForeignKey('Warehouse', related_name='containers', null=False, blank=False)
    commodity = models.ForeignKey('catalogue.BoardGameCommodity', related_name='containers', null=False, blank=False)
    total = models.IntegerField()

    def __str__(self):
        return self.commodity.__str__()

    @property
    def available(self):
        return self.total - self.clienthasboardgame_set.filter(returned=None).count()

    class Meta:
        unique_together = ('warehouse', 'commodity')
