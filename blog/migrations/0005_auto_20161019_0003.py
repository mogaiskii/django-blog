# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 17:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20161016_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='last_edit_date',
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 18, 17, 3, 10, 806870, tzinfo=utc)),
        ),
    ]
