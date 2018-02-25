from django.contrib import admin
from catalogue.models import BoardGameItem, BoardGameCommodity

# Register your models here.
admin.site.register (BoardGameItem)
admin.site.register (BoardGameCommodity)
