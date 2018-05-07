# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-02 09:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0025_auto_20180502_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='scanner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webscans', to='os2webscanner.Scanner', verbose_name='webscanner'),
        ),
    ]
