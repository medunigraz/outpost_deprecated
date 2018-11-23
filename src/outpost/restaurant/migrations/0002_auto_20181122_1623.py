# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-22 15:23
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseExtractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('dateformat', models.CharField(max_length=64)),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
        ),
        migrations.CreateModel(
            name='XMLRestaurant',
            fields=[
                ('restaurant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='restaurant.Restaurant')),
                ('source', models.URLField()),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('restaurant.restaurant',),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_restaurant.restaurant_set+', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='diet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Diet'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='foreign',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='foreign',
            field=models.CharField(blank=True, db_index=True, max_length=256, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='position',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, null=True, srid=3857),
        ),
        migrations.CreateModel(
            name='XSLTExtractor',
            fields=[
                ('baseextractor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='restaurant.BaseExtractor')),
                ('xslt', models.TextField()),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('restaurant.baseextractor',),
        ),
        migrations.AddField(
            model_name='xmlrestaurant',
            name='extractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.BaseExtractor'),
        ),
        migrations.AddField(
            model_name='baseextractor',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_restaurant.baseextractor_set+', to='contenttypes.ContentType'),
        ),
    ]
