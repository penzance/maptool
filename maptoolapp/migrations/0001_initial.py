# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource_link_id', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('organization', models.CharField(max_length=100)),
                ('first_name_permission', models.BooleanField(default=False)),
                ('last_name_permission', models.BooleanField(default=False)),
                ('email_permission', models.BooleanField(default=False)),
                ('organization_permission', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('mapurl', models.CharField(max_length=200)),
                ('generated_latitude', models.CharField(max_length=50)),
                ('generated_longitude', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('locality', models.CharField(max_length=50)),
                ('method', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='locations',
            unique_together=set([('resource_link_id', 'user_id')]),
        ),
    ]
