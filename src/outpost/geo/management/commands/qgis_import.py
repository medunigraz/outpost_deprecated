from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.gdal import DataSource
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from ... import models
from outpost.campusonline import models as co


class Command(BaseCommand):
    help = 'Import and transform objects from QGIS schema'

    def add_arguments(self, parser):
        parser.add_argument('-d', nargs='*')
        parser.add_argument('-r', nargs='*')
        parser.add_argument('-f', nargs='*')
        parser.add_argument('-b', nargs='*')

    def handle(self, *args, **options):
        if options.get('b'):
            for building in options.get('b'):
                self.buildings(DataSource(building))
        if options.get('f'):
            for building in options.get('f'):
                self.floors(DataSource(building))
        if options.get('d'):
            for building in options.get('d'):
                self.doors(DataSource(building))
        if options.get('r'):
            for building in options.get('r'):
                self.rooms(DataSource(building))

    def doors(self, source):
        for layer in source:
            self.stdout.write('Layer: {}'.format(layer.name))
            for feature in layer:
                defaults = {
                    'origin': feature.get('id'),
                    'layout': feature.geom.geos,
                    'floor': models.Floor.objects.get(pk=feature.get('floor_id'))
                }
                obj, created = models.Door.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created door {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated door {}'.format(obj))
                self.stdout.write(msg)

    def rooms(self, source):
        for layer in source:
            self.stdout.write('Layer: {}'.format(layer.name))
            for feature in layer:
                defaults = {
                    'origin': feature.get('id'),
                    'layout': feature.geom.geos,
                    'floor': models.Floor.objects.get(pk=feature.get('floor_id'))
                }
                if feature.get('campusonli'):
                    try:
                        defaults['campusonline'] = co.Room.objects.get(name_full=feature.get('campusonli'))
                    except co.Room.DoesNotExist as e:
                        defaults['campusonline'] = None
                obj, created = models.Room.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created room {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated room {}'.format(obj))
                self.stdout.write(msg)

    def floors(self, source):
        for layer in source:
            self.stdout.write('Layer: {}'.format(layer.name))
            for feature in layer:
                defaults = {
                    'origin': feature.get('id'),
                    'outline': MultiPolygon(feature.geom.geos),
                    'building': models.Building.objects.get(pk=feature.get('building_i'))
                }
                obj, created = models.Floor.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created floor {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated floor {}'.format(obj))
                self.stdout.write(msg)

    def buildings(self, source):
        for layer in source:
            self.stdout.write('Layer: {}'.format(layer.name))
            for feature in layer:
                defaults = {
                    'origin': feature.get('id'),
                    'outline': MultiPolygon(feature.geom.geos)
                }
                if feature.get('campusonli'):
                    try:
                        defaults['campusonline'] = co.Building.objects.get(short=feature.get('campusonli'))
                    except co.Room.DoesNotExist as e:
                        defaults['campusonline'] = None
                obj, created = models.Building.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created building {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated building {}'.format(obj))
                self.stdout.write(msg)
