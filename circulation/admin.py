from django.contrib import admin
from circulation.models import (RentalClient, ClientID)

class ClientIDAdmin(admin.StackedInline):
    model = ClientID
    extra = 0

class RentalClientAdmin(admin.ModelAdmin):
    inlines = [ClientIDAdmin]