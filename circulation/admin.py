from django.contrib import admin
from circulation.models import (RentalClient, ClientID, BoardGameLending)

# Register your models here.
admin.site.register (RentalClient)
admin.site.register (ClientID)
admin.site.register (BoardGameLending)


# class ClientIDAdmin(admin.StackedInline):
#     model = ClientID
#     extra = 0
#
# class RentalClientAdmin(admin.ModelAdmin):
#     inlines = [ClientIDAdmin]
