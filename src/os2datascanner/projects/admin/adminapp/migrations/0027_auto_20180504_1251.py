# Generated by Django 1.11.9 on 2018-05-04 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0026_auto_20180502_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedomain',
            name='mountname',
        ),
        migrations.AddField(
            model_name='filedomain',
            name='mountpath',
            field=models.CharField(max_length=2048, null=True, verbose_name='Folder sti'),
        ),
    ]
