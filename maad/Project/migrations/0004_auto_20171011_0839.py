# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-11 08:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0003_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='urldata',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
