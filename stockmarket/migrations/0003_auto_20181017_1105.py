# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-17 05:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0002_auto_20181017_1039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='_type',
            new_name='order_type',
        ),
    ]
