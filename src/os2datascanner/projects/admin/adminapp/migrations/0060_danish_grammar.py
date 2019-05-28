# Generated by Django 1.11.20 on 2019-04-11 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0059_auto_20190404_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authentication',
            name='domain',
            field=models.CharField(blank=True, default='', max_length=2024, verbose_name='Brugerdomæne'),
        ),
        migrations.AlterField(
            model_name='authentication',
            name='username',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='Brugernavn'),
        ),
        migrations.AlterField(
            model_name='conversionqueueitem',
            name='status',
            field=models.CharField(choices=[('NEW', 'Ny'), ('PROCESSING', 'I gang'), ('FAILED', 'Mislykket')], default='NEW', max_length=10, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='authentication',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='os2webscanner_domain_authentication', to='os2webscanner.Authentication', verbose_name='Brugernavn'),
        ),
        migrations.AlterField(
            model_name='exchangescanner',
            name='domains',
            field=models.ManyToManyField(related_name='exchangedomains', to='os2webscanner.ExchangeDomain', verbose_name='Exchangedomæner'),
        ),
        migrations.AlterField(
            model_name='filescanner',
            name='domains',
            field=models.ManyToManyField(related_name='filedomains', to='os2webscanner.FileDomain', verbose_name='Fildomæner'),
        ),
        migrations.AlterField(
            model_name='scan',
            name='status',
            field=models.CharField(choices=[('NEW', 'Ny'), ('STARTED', 'I gang'), ('DONE', 'Færdig'), ('FAILED', 'Mislykket')], default='NEW', max_length=10),
        ),
        migrations.AlterField(
            model_name='scanner',
            name='do_last_modified_check',
            field=models.BooleanField(default=True, verbose_name='Tjek dato for sidste ændring'),
        ),
        migrations.AlterField(
            model_name='scanner',
            name='regex_rules',
            field=models.ManyToManyField(blank=True, to='os2webscanner.RegexRule', verbose_name='Regex-regler'),
        ),
        migrations.AlterField(
            model_name='webscanner',
            name='do_last_modified_check_head_request',
            field=models.BooleanField(default=True, verbose_name='Brug HTTP HEAD-forespørgsler'),
        ),
        migrations.AlterField(
            model_name='webscanner',
            name='domains',
            field=models.ManyToManyField(related_name='webdomains', to='os2webscanner.WebDomain', verbose_name='Webdomæner'),
        ),
    ]
