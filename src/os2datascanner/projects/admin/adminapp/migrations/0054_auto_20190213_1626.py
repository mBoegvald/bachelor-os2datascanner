# Generated by Django 1.11.14 on 2019-02-13 15:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0053_auto_20190206_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanner',
            name='do_cpr_ignore_irrelevant',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='do_cpr_modulus11',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='do_cpr_scan',
        ),
    ]
