import logging
from datetime import timedelta
from decimal import Decimal
from email.utils import parsedate_to_datetime

import requests
from celery.task import PeriodicTask
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from geopy.geocoders import Nominatim
from requests.exceptions import RequestException

from . import models

logger = logging.getLogger(__name__)


class RestaurantSyncTask(PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self, **kwargs):
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
                obj, created = models.Meal.objects.update_or_create(
                    foreign=int(meal.get('uid')),
                    defaults={
                        'foreign': int(meal.get('uid')),
                        'restaurant': rest,
                        'available': parsedate_to_datetime(meal.get('date')),
                        'description': meal.get('description'),
                        'price': Decimal(meal.get('price')),
                        'diet': diets.get(meal.get('diet')),
                    }
                )
                if created:
                    logger.info(f'Created new meal: {obj}')
