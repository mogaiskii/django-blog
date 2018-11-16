# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-15 02:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dislikes',
            field=models.ManyToManyField(related_name='disliker', to='blog.Post'),
        ),
        migrations.AddField(
            model_name='profile',
            name='likes',
            field=models.ManyToManyField(related_name='liker', to='blog.Post'),
        ),
        migrations.AddField(
            model_name='profile',
            name='score',
            field=models.IntegerField(default=20),
        ),
    ]