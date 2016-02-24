# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('home', models.CharField(max_length=255)),
                ('visitor', models.CharField(max_length=255)),
                ('price_1', models.FloatField()),
                ('price_x', models.FloatField()),
                ('price_2', models.FloatField()),
            ],
        ),
    ]
