# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-10 06:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(blank=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('project_type', models.CharField(choices=[('business scope', 'Business Scope'), ('history', 'History'), ('change in capital', 'Change in Capital'), ('share with voting right', 'Share with Voting Right'), ('dividend', 'Dividend')], default='A', max_length=15)),
                ('project_field', models.CharField(max_length=50)),
                ('project_co', models.CharField(max_length=20)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('project_tool', models.CharField(choices=[('business scope', 'Business Scope'), ('history', 'History'), ('change in capital', 'Change in Capital'), ('share with voting right', 'Share with Voting Right'), ('dividend', 'Dividend')], default='A', max_length=15)),
                ('description', models.TextField(blank=True)),
                ('project_result', models.TextField(blank=True)),
            ],
        ),
    ]