from django.contrib import admin
from circulation.models import (Customer, CustomerID, BoardGameLending)

# Register your models here.
admin.site.register (Customer)
admin.site.register (CustomerID)
admin.site.register (BoardGameLending)


# class ClientIDAdmin(admin.StackedInline):
#     model = ClientID
#     extra = 0
#
# class CustomerAdmin(admin.ModelAdmin):
#     inlines = [ClientIDAdmin]
