from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Item(BaseModel):
    QUANTITY_TYPE = {
        '1': 'kg',
        '2': 'vnt.'
    }

    title = models.CharField(max_length=128)
    quantity = models.FloatField()
    quantity_type = models.CharField(max_length=50, choices=QUANTITY_TYPE, default='1')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    def __str__(self):
        return f'{self.title}'

    def get_quantity_type_value(self):
        return self.QUANTITY_TYPE[self.quantity_type]
