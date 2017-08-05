from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.utils import timezone
from tqdm import tqdm

from outpost.campusonline import models as co

from ... import models


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
        now = timezone.now()
        tsource = tqdm(source)
        tsource.desc = 'Doors'
        for layer in source:
            tlayer = tqdm(layer)
            tlayer.desc = layer.name
            for feature in tlayer:
                fl_id = feature.get('floor_id')
                defaults = {
                    'origin': feature.get('id'),
                    'layout': feature.geom.geos,
                    'level': models.Floor.objects.get(origin=fl_id).level,
                    'deprecated': False
                }
                obj, created = models.Door.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )
        models.Door.objects.filter(modified__lt=now).update(deprecated=True)

    def rooms(self, source):
        now = timezone.now()
        tsource = tqdm(source)
        tsource.desc = 'Rooms'
        for layer in source:
            tlayer = tqdm(layer)
            tlayer.desc = layer.name
            for feature in tlayer:
                co_id = feature.get('campusonli')
                fl_id = feature.get('floor_id')
                defaults = {
                    'origin': feature.get('id'),
                    'layout': feature.geom.geos,
                    'level': models.Floor.objects.get(origin=fl_id).level,
                    'deprecated': False
                }
                if co_id:
                    template = '{f.building.campusonline.short}{f.campusonline.short}.{c:03d}'
                    try:
                        f = models.Floor.objects.get(origin=fl_id)
                        name = template.format(f=f, c=int(co_id))
                        defaults['campusonline'] = co.Room.objects.get(name_full=name)
                    except co.Room.DoesNotExist as e:
                        defaults['campusonline'] = None
                    except ValueError as e:
                        defaults['campusonline'] = None
                        self.stdout.write(
                            self.style.ERROR(
                                'Unable to parse CO identifier: {}'.format(co_id)
                            )
                        )

                obj, created = models.Room.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )
        models.Room.objects.filter(modified__lt=now).update(deprecated=True)

    def floors(self, source):
        tsource = tqdm(source)
        tsource.desc = 'Floors'
        for layer in source:
            tlayer = tqdm(layer)
            tlayer.desc = layer.name
            for feature in tlayer:
                b = models.Building.objects.get(origin=feature.get('building_i'))
                name = '{b.campusonline.short}{n}'
                defaults = {
                    'origin': feature.get('id'),
                    'outline': MultiPolygon(feature.geom.geos),
                    'building': b,
                    'name': name.format(b=b, n=feature.get('name').split('.')[-1])
                }
                short = feature.get('name').split('.')[-1]
                try:
                    defaults['campusonline'] = co.Floor.objects.get(short=short)
                except co.Floor.DoesNotExist as e:
                    defaults['campusonline'] = None
                obj, created = models.Floor.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )

    def buildings(self, source):
        tsource = tqdm(source)
        tsource.desc = 'Buildings'
        for layer in source:
            tlayer = tqdm(layer)
            tlayer.desc = layer.name
            for feature in tlayer:
                defaults = {
                    'origin': feature.get('id'),
                    'outline': MultiPolygon(feature.geom.geos)
                }
                if feature.get('campusonli'):
                    try:
                        defaults['campusonline'] = co.Building.objects.get(short=feature.get('campusonli'))
                    except co.Building.DoesNotExist as e:
                        defaults['campusonline'] = None
                obj, created = models.Building.objects.update_or_create(
                    origin=feature.get('id'),
                    defaults=defaults
                )
