import logging

from django.conf import settings
from django.contrib.gis.db import models

logger = logging.getLogger(__name__)


class Diet(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of diet.
    '''
    name = models.CharField(
        max_length=128
    )
    foreign = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of doctoral school.

    ### `address` (`string`)
    Street address.

    ### `zipcode` (`string`)
    Zip code.

    ### `city` (`string`)
    City.

    ### `phone` (`string`)
    Phone.

    ### `email` (`string`)
    Email address.

    ### `url` (`string`)
    Homepage URL.

    ### `position` (`Object`)
    Location of restaurant on map as [GeoJSON](http://geojson.org/).
    '''
    name = models.CharField(
        max_length=128
    )
    foreign = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=128
    )
    zipcode = models.CharField(
        max_length=16
    )
    city = models.CharField(
        max_length=128
    )
    phone = models.CharField(
        max_length=64
    )
    email = models.EmailField()
    url = models.URLField(
        blank=True,
        null=True,
    )
    position = models.PointField(
        blank=True,
        null=True,
        srid=settings.DEFAULT_SRID
    )

    def __str__(self):
        return self.name


class Meal(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `description` (`string`)
    Description of meal.

    ### `restaurant` (`integer` or `Object`)
    Foreign key to [Restaurant](../restaurant) this meal is served at.

    ### `price` (`number`)
    Price of meal.

    ### `diet` (`integer` or `Object`)
    Foreign key to [Diet](../diet) this meal is conformant with.
    '''
    foreign = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    restaurant = models.ForeignKey(
        'Restaurant',
        related_name='meals'
    )
    available = models.DateField()
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    diet = models.ForeignKey(
        'Diet'
    )

    def __str__(self):
        return self.description
