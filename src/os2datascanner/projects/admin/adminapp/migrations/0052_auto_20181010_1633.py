# Generated by Django 1.11.14 on 2018-10-10 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0051_auto_20181009_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='do_cpr_ignore_irrelevant',
            field=models.BooleanField(default=True, verbose_name='Ignorer ugyldige fødselsdatoer'),
        ),
        migrations.AddField(
            model_name='scan',
            name='do_cpr_modulus11',
            field=models.BooleanField(default=True, verbose_name='Tjek modulus-11'),
        ),
        migrations.AddField(
            model_name='scan',
            name='do_cpr_scan',
            field=models.BooleanField(default=True, verbose_name='CPR'),
        ),
        migrations.AddField(
            model_name='scanner',
            name='do_cpr_ignore_irrelevant',
            field=models.BooleanField(default=True, verbose_name='Ignorer ugyldige fødselsdatoer'),
        ),
        migrations.AddField(
            model_name='scanner',
            name='do_cpr_modulus11',
            field=models.BooleanField(default=True, verbose_name='Tjek modulus-11'),
        ),
        migrations.AddField(
            model_name='scanner',
            name='do_cpr_scan',
            field=models.BooleanField(default=True, verbose_name='CPR'),
        ),
    ]
