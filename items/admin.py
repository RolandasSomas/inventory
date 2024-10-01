from django.contrib import admin

# Register your models here.
from .models import Item, Location, ItemAction, ItemType, ItemCategory

admin.site.register(Item)
admin.site.register(Location)
admin.site.register(ItemAction)
admin.site.register(ItemType)
admin.site.register(ItemCategory)