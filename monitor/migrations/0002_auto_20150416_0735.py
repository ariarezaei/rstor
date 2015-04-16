# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='Throughput',
        ),
        migrations.AddField(
            model_name='log',
            name='throughput_read',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='throughput_write',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='mean_read_time',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='mean_write_time',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='read_hit_rate',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='read_requests',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='time',
            field=models.TimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='write_hit_rate',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='write_requests',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
