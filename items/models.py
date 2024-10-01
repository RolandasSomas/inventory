from contextlib import nullcontext
from datetime import datetime
from email.policy import default

import django
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class ItemCategory(BaseModel):
    title = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.title}'


class ItemType(BaseModel):
    QUANTITY_TYPE = {
        '1': 'kg',
        '2': 'vnt.'
    }
    id_number = models.CharField(max_length=12, blank=True, verbose_name="Serial number")
    title = models.CharField(max_length=128)
    price = models.FloatField(default=0)
    quantity_type = models.CharField(max_length=50, choices=QUANTITY_TYPE, default='1')
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, related_name='category')

    def __str__(self):
        return f'{self.title}'

    def get_quantity_type_value(self):
        return self.QUANTITY_TYPE[self.quantity_type]



class Item(BaseModel):

    quantity = models.FloatField()
    item_type = models.ForeignKey(ItemType, on_delete=models.DO_NOTHING, related_name='item_name', null=True, verbose_name='Item name')
    created_on = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='items')
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='location', null=True, blank=True)
    from_location = models.CharField(max_length=128, default="", verbose_name="Arrived from")

    def total_price(self):
        if self.item_type:
            return self.item_type.price * self.quantity
        else:
            return "-"


class ItemAction(BaseModel):
    ACTION = {
        '1': 'Added',
        '2': 'Removed',
        '3': 'Moved'
    }
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item')
    date = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True)
    amount = models.FloatField()
    from_location = models.CharField(max_length=128, default="")
    action = models.CharField(max_length=50, choices=ACTION, default='1')
    move_to = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='move_to', blank=True, null=True)
    created_by = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING, related_name='created_by')
    reason = models.TextField(max_length=1024, default="")

    def get_action_value(self):
        return self.ACTION[self.action]
