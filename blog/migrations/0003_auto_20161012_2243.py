# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 15:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20161012_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rate',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 12, 15, 43, 8, 723018, tzinfo=utc)),
        ),
    ]