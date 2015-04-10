# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context_id', models.CharField(max_length=50)),
                ('resource_link_id', models.CharField(max_length=50)),
                ('custom_canvas_course_id', models.CharField(max_length=50)),
                ('item_name', models.CharField(max_length=50)),
                ('item_description', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locality', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('generated_longitude', models.CharField(max_length=50)),
                ('generated_latitude', models.CharField(max_length=50)),
                ('method', models.CharField(max_length=10)),
                ('datetime', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('info', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('mapurl', models.CharField(max_length=200)),
                ('itemgroup', models.ForeignKey(to='maptoolapp.ItemGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_1', models.CharField(max_length=250)),
                ('generated_longitude_1', models.CharField(max_length=50)),
                ('generated_latitude_1', models.CharField(max_length=50)),
                ('description_1', models.CharField(max_length=250)),
                ('url_2', models.CharField(max_length=250)),
                ('generated_longitude_2', models.CharField(max_length=50)),
                ('generated_latitude_2', models.CharField(max_length=50)),
                ('description_2', models.CharField(max_length=250)),
                ('url_3', models.CharField(max_length=250)),
                ('generated_longitude_3', models.CharField(max_length=50)),
                ('generated_latitude_3', models.CharField(max_length=50)),
                ('description_3', models.CharField(max_length=250)),
                ('itemgroup', models.ForeignKey(to='maptoolapp.ItemGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
