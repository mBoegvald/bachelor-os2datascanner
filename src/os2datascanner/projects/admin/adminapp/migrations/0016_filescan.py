# Generated by Django 1.11.9 on 2018-05-01 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0015_auto_20180501_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileScan',
            fields=[
                ('scan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='os2webscanner.Scan')),
                ('domains', models.ManyToManyField(to='os2webscanner.FileDomain', verbose_name='Domæner')),
                ('scanner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filescans', to='os2webscanner.FileScanner', verbose_name='filescanner')),
            ],
            options={
                'db_table': 'os2webscanner_filescan',
            },
            bases=('os2webscanner.scan',),
        ),
    ]
