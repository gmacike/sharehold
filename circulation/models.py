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
        

class ClientID (models.Model):
    rentalClient = models.ForeignKey ('RentalClient',
        on_delete = models.CASCADE, related_name = 'client', null = True, blank = False)
    ID = models.IntegerField ( primary_key = True, unique = True )
    active = models.BooleanField (default = True)
    
    
    