# Generated by Django 1.11.20 on 2019-03-13 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0057_merge_20190307_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='matched_data',
            field=models.TextField(verbose_name='Data match'),
        ),
    ]
