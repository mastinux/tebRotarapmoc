# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rotarapmoc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='origin',
            field=models.CharField(default='adfasdf', max_length=255),
            preserve_default=False,
        ),
    ]
