# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-14 06:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moderator',
            name='big_boss',
        ),
        migrations.RemoveField(
            model_name='moderator',
            name='blog',
        ),
        migrations.RemoveField(
            model_name='moderator',
            name='user',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='moderators',
        ),
        migrations.AddField(
            model_name='blog',
            name='description',
            field=models.TextField(default='Description'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Moderator',
        ),
    ]
