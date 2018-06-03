from django.core.validators import MinValueValidator, MaxValueValidator
from django.apps import apps
from django.db import models
from django.db.models import Sum



class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    def catalogueItems (self):
        model = apps.get_model('catalogue', 'BoardGameItem')
        return model.objects.filter(commodities__containers__warehouse=self)

    def catalogueItemsCount (self):
        agg = BoardGameContainer.objects.filter(warehouse=self).count()
        if agg == None:
            return 0
        return agg

    def commoditiesTotalCount (self):
        agg = BoardGameContainer.objects.filter(warehouse=self).aggregate(total=Sum('total'))
        total = agg ['total']
        if total == None:
            return 0
        return total

    def commoditiesAvailableCount (self):
        available = 0
        containers = BoardGameContainer.objects.filter(warehouse=self)
        if containers.exists():
            for container in containers:
                available += container.available
        return available

    def getDesc (self):
        if self.desc != "":
            return self.desc
        else:
            return "Brak dodatkowych informacji."


class BoardGameContainer(models.Model):
    warehouse = models.ForeignKey('Warehouse', related_name='containers', null=False, blank=False)
    commodity = models.ForeignKey('catalogue.BoardGameCommodity', related_name='containers', null=False, blank=False)
    total = models.IntegerField(validators=[MinValueValidator(0), ])

    def __str__(self):
        return self.commodity.__str__() + "@" + self.warehouse.__str__()

    @property
    def available(self):
        return self.total - self.boardgamelending_set.filter(returned=None).count()

    class Meta:
        unique_together = ('warehouse', 'commodity')
