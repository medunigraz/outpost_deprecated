from shapely.affinity import affine_transform
from shapely.wkb import loads

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from ... import models
from outpost.campusonline import models as co


class Command(BaseCommand):
    help = 'Import and transform objects from QGIS schema'
    # matrix = [
    #     -0.709557,
    #     -1.351259,
    #     0.709557,
    #     -1.351259,
    #     1722129.009,
    #     5959995.217
    # ]
    # srid = 3857

    def add_arguments(self, parser):
        parser.add_argument('-s', type=int, required=False, default=settings.DEFAULT_SRID)
        parser.add_argument('-a', type=float, required=True)
        parser.add_argument('-b', type=float, required=True)
        parser.add_argument('-d', type=float, required=True)
        parser.add_argument('-e', type=float, required=True)
        parser.add_argument('-x', type=float, required=True)
        parser.add_argument('-y', type=float, required=True)

    def handle(self, *args, **options):
        self.matrix = list(map(lambda k: options[k], ['a', 'b', 'd', 'e', 'x', 'y']))
        self.srid = options['s']
        self.buildings()

    def transform(self, geom):
        af = affine_transform(loads(bytes.fromhex(geom)), self.matrix)
        return GEOSGeometry(memoryview(af.wkb), self.srid)

    def doors(self, floor):
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id, layout FROM qgis.door WHERE floor_id = %s',
                [floor.origin]
            )
            for r in cursor:
                defaults = {
                    'origin': r[0],
                    'layout': self.transform(r[1]),
                    'floor': floor
                }
                obj, created = models.Door.objects.update_or_create(
                    origin=r[0],
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created door {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated door {}'.format(obj))
                self.stdout.write(msg)

    def rooms(self, floor):
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id, layout, campusonline FROM qgis.room WHERE floor_id = %s',
                [floor.origin]
            )
            for r in cursor:
                defaults = {
                    'origin': r[0],
                    'layout': self.transform(r[1]),
                    'floor': floor
                }
                if r[2]:
                    try:
                        defaults['campusonline'] = co.Room.objects.get(name_full=r[2])
                    except co.Room.DoesNotExist as e:
                        defaults['campusonline'] = None
                obj, created = models.Room.objects.update_or_create(
                    origin=r[0],
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created room {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated room {}'.format(obj))
                self.stdout.write(msg)

    def floors(self, building):
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id, layout FROM qgis.floor WHERE building_id = %s',
                [building.origin]
            )
            for r in cursor:
                defaults = {
                    'origin': r[0],
                    'outline': self.transform(r[1]),
                    'building': building
                }
                obj, created = models.Floor.objects.update_or_create(
                    origin=r[0],
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created floor {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated floor {}'.format(obj))
                self.stdout.write(msg)
                self.doors(obj)
                self.rooms(obj)

    def buildings(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, layout, campusonline FROM qgis.building')
            for r in cursor:
                defaults = {
                    'origin': r[0],
                    'outline': self.transform(r[1]),
                }
                if r[2]:
                    try:
                        defaults['campusonline'] = co.Building.objects.get(short=r[2])
                    except co.Room.DoesNotExist as e:
                        defaults['campusonline'] = None
                obj, created = models.Building.objects.update_or_create(
                    origin=r[0],
                    defaults=defaults
                )
                if created:
                    msg = self.style.SUCCESS('Created building {}'.format(obj))
                else:
                    msg = self.style.SUCCESS('Updated building {}'.format(obj))
                self.stdout.write(msg)
                self.floors(obj)
