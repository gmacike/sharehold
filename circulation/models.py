from django.db import models

class RentalClient (models.Model):
    identificationCode = models.IntegerField ( unique = True )
    initials = models.CharField ( max_length = 10 )

    def getIdentificationCode (self):
        return self.identificationCode
        
    def setIdentificationCode (self, identificationCode):
        self.identificationCode = identificationCode
        
    def getInitials (self):
        return self.initials
        
    def setInitials (self, initials):
        self.initials = initials
    