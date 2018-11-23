import json
import logging
from collections import defaultdict
from datetime import timedelta
from decimal import (
    Decimal,
    InvalidOperation,
)
from email.utils import parsedate_to_datetime
from hashlib import sha256
from time import strptime

import requests
from celery.task import PeriodicTask
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from geopy.geocoders import Nominatim
from lxml import etree
from requests.exceptions import RequestException

from . import models

logger = logging.getLogger(__name__)


class RestaurantSyncTask(PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self, **kwargs):
        today = timezone.localdate()
        self.json()
        self.xml()
        models.Meal.objects.exclude(available=today).delete()

    def json(self):
        today = timezone.localdate()
        url = settings.OUTPOST.get('restaurants')
        if not url:
            logger.debug('No URL for restaurant sync defined, skipping.')
            return
        try:
            req = requests.get(
                url,
                headers={
                    'Accept': 'application/json',
                }
            )
            req.raise_for_status()
        except RequestException as e:
            logger.warn(f'Could not fetch restaurant data: {e}')
            return
        menu = req.json().get('menu')
        if not menu:
            logger.warn('No "menu" attribute found in restaurant data.')
            return
        date = parsedate_to_datetime(menu.get('date'))
        if date:
            logger.debug(f'Processing restaurant menu from {date}')
        diets = {}
        for foreign, name in menu.get('diet', {}).items():
            obj, created = models.Diet.objects.update_or_create(
                foreign=int(foreign),
                defaults={
                    'foreign': int(foreign),
                    'name': name,
                }
            )
            if created:
                logger.info(f'Created new diet: {obj}')
            diets[int(foreign)] = obj
        nom = Nominatim(user_agent=__name__)
        for data in menu.get('restaurants', {}):
            position = nom.geocode(
                {
                    'street': data.get('address'),
                    'city': data.get('city'),
                    'country': 'Austria',  # TODO: No hardcoded country ... find a way to autolocate
                    'postalcode': data.get('zip'),
                },
                geometry='wkt'
            )
            rest, created = models.Restaurant.objects.update_or_create(
                foreign=int(data.get('uid')),
                defaults={
                    'foreign': int(data.get('uid')),
                    'name': data.get('company'),
                    'address': data.get('address'),
                    'zipcode': data.get('zip'),
                    'city': data.get('city'),
                    'phone': data.get('telephone'),
                    'email': data.get('email'),
                    'url': data.get('www') or None,
                    'position': GEOSGeometry(
                        position.raw.get('geotext'),
                        srid=4326  # TODO: Setting for SRID
                    ).centroid
                }
            )
            if created:
                logger.info(f'Created new restaurant: {rest}')
            for meal in data.get('meals', {}):
                available = parsedate_to_datetime(meal.get('date'))
                if today != available.date():
                    continue
                obj, created = models.Meal.objects.update_or_create(
                    foreign=meal.get('uid'),
                    defaults={
                        'foreign': meal.get('uid'),
                        'restaurant': rest,
                        'available': available,
                        'description': meal.get('description'),
                        'price': Decimal(meal.get('price')),
                        'diet': diets.get(meal.get('diet')),
                    }
                )
                if created:
                    logger.info(f'Created new meal: {obj}')
        logger.debug(f'Removing meals not available today: {today}')

    def xml(self):
        today = timezone.localdate()
        for xrest in models.XMLRestaurant.objects.filter(enabled=True):
            try:
                req = requests.get(
                    xrest.url,
                    headers={
                        'Accept': 'text/xml',
                    }
                )
                req.raise_for_status()
            except RequestException as e:
                logger.warn(f'Could not fetch restaurant data: {e}')
                return
            doc = etree.XML(req.text)
            transformer = etree.XSLT(etree.XML(xrest.extractor.xslt))
            data = transformer(doc)
            for meal in json.loads(str(data)):
                values = defaultdict(lambda: None)
                values.update(meal)
                if 'available' in meal:
                    values['available'] = strptime(
                        meal.get('available'),
                        xrest.dateformat
                    ).date()
                    if values['available'] != today:
                        continue
                else:
                    values['available'] = today
                if 'foreign' not in meal:
                    logger.info(f'No foreign key data found: {meal}')
                    continue
                values['foreign'] = sha256(meal.get('foreign')).hexdigest()
                if meal.get('price'):
                    try:
                        values['price'] = Decimal(meal.get('price'))
                    except InvalidOperation as e:
                        logger.info(f'Could not convert to Decimal: {e}')
                        values['price'] = None
                if meal.get('diet'):
                    try:
                        diet_pk = int(meal.get('diet'))
                    except ValueError as e:
                        logger.info(f'Could not convert diet primary key: {e}')
                    else:
                        try:
                            values['diet'] = models.Diet.objects.get(pk=diet_pk)
                        except models.Diet.DoesNotExist:
                            logger.info(f'Diet not found: {diet_pk}')
                            values['diet'] = None
                values['restaurant'] = xrest

                obj, created = models.Meal.objects.update_or_create(
                    foreign=values['foreign'],
                    defaults=values
                )
                if created:
                    logger.info(f'Created new meal: {obj}')
