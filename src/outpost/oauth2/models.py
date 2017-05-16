from django.db import models
from django.core.validators import URLValidator
from oauth2_provider.models import AbstractApplication


class Application(AbstractApplication):
    logo = models.ImageField()
    agree = models.BooleanField()
    website = models.TextField(validators=[URLValidator()])
    privacy = models.TextField(validators=[URLValidator()])
    description = models.TextField()
