# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-02-06 12:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0052_auto_20181010_1633'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='md5sum',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='md5sum',
            name='organization',
        ),
        migrations.DeleteModel(
            name='Md5Sum',
        ),
    ]
