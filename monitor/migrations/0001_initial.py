# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('time', models.TimeField(verbose_name='Log Date')),
                ('date', models.DateField(verbose_name='Log Time')),
                ('read_hit_rate', models.FloatField()),
                ('write_hit_rate', models.FloatField()),
                ('Throughput', models.FloatField()),
                ('mean_write_time', models.FloatField()),
                ('mean_read_time', models.FloatField()),
                ('write_requests', models.IntegerField()),
                ('read_requests', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
