# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('group', models.CharField(max_length=200)),
                ('topic', models.CharField(max_length=200)),
                ('series_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('api_key', models.CharField(max_length=200)),
                ('token', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='cluster',
            field=models.ForeignKey(to='clusters.Cluster'),
        ),
    ]
