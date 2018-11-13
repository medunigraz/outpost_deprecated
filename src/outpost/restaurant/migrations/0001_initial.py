# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-08 19:00
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('foreign', models.PositiveIntegerField(blank=True, null=True)),
                ('available', models.DateField()),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('diet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Diet')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('foreign', models.PositiveIntegerField(blank=True, null=True)),
                ('address', models.CharField(max_length=128)),
                ('zipcode', models.CharField(max_length=16)),
                ('city', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('url', models.URLField(blank=True, null=True)),
                ('position', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=3857)),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='restaurant.Restaurant'),
        ),
    ]