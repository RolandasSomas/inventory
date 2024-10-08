# Generated by Django 5.1.1 on 2024-09-22 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_itemcategory_remove_item_id_number_remove_item_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category', to='items.itemcategory'),
        ),
    ]
