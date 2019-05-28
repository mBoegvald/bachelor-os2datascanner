# Generated by Django 1.11.14 on 2018-10-09 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0049_merge_20180919_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchangescan',
            name='folder_to_scan',
        ),
        migrations.RemoveField(
            model_name='exchangescan',
            name='last_scannings_date',
        ),
        migrations.RemoveField(
            model_name='exchangescan',
            name='mark_scan_as_done',
        ),
        migrations.RemoveField(
            model_name='exchangescanner',
            name='last_scannings_date',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='do_cpr_ignore_irrelevant',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='do_cpr_modulus11',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='do_cpr_scan',
        ),
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
        migrations.AddField(
            model_name='exchangescanner',
            name='dir_to_scan',
            field=models.CharField(max_length=2048, null=True, verbose_name='Exchange export sti'),
        ),
        migrations.AddField(
            model_name='exchangescanner',
            name='is_exporting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exchangescanner',
            name='is_ready_to_scan',
            field=models.BooleanField(default=False),
        ),
    ]
