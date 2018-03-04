from django.db import models

from warehouse.models import BoardGameContainer


class RentalClient(models.Model):
    identificationCode = models.IntegerField(unique=True)
    initials = models.CharField(max_length=10)

    def __str__(self):
        return '{} {}'.format(self.initials, self.identificationCode)

    def getIdentificationCode(self):
        return self.identificationCode

    def setIdentificationCode(self, identificationCode):
        self.identificationCode = identificationCode

    def getInitials(self):
        return self.initials

    def setInitials(self, initials):
        self.initials = initials


class ClientHasBoardGame(models.Model):
    client = models.ForeignKey(RentalClient)
    container = models.ForeignKey(BoardGameContainer)
