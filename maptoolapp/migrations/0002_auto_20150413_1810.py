# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maptoolapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='urls',
            name='zoom_1',
            field=models.CharField(default=8, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urls',
            name='zoom_2',
            field=models.CharField(default=7, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urls',
            name='zoom_3',
            field=models.CharField(default=8, max_length=50),
            preserve_default=False,
        ),
    ]
