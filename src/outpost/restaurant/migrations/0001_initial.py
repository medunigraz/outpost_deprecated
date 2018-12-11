# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-11 08:26
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
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
            name='Diet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('foreign', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign', models.CharField(max_length=256)),
                ('available', models.DateField()),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('diet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Diet')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('foreign', models.CharField(blank=True, db_index=True, max_length=256, null=True, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('zipcode', models.CharField(max_length=16)),
                ('city', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('url', models.URLField(blank=True, null=True)),
                ('position', django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, null=True, srid=3857)),
                ('enabled', models.BooleanField(default=False)),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
        ),
        migrations.CreateModel(
            name='XMLRestaurant',
            fields=[
                ('restaurant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='restaurant.Restaurant')),
                ('source_template', models.TextField()),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('restaurant.restaurant',),
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
            model_name='restaurant',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_restaurant.restaurant_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='meal',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='restaurant.Restaurant'),
        ),
        migrations.AddField(
            model_name='baseextractor',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_restaurant.baseextractor_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='xmlrestaurant',
            name='extractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.BaseExtractor'),
        ),
    ]
