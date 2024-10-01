# Generated by Django 5.1.1 on 2024-09-16 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_alter_itemaction_move_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemaction',
            name='move_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='move_to', to='items.location'),
        ),
    ]
