import logging
from datetime import datetime

from django.core.cache import cache
from oauthlib.oauth1 import RequestValidator

from . import models
from .conf import settings

logger = logging.getLogger(__name__)


class OutpostRequestValidator(RequestValidator):

    dummy_client = settings.LTI_DUMMY_CLIENT
    client_key_length = settings.LTI_CLIENT_KEY_LENGTH
    nonce_length = settings.LTI_NONCE_LENGTH

    def get_client_secret(self, client_key, request):
        try:
            return models.Consumer.objects.get(key=client_key).secret
        except models.Consumer.DoesNotExist:
            return settings.LTI_DUMMY_SECRET

    def get_rsa_key(self, client_key, request):
        try:
            return models.Consumer.objects.get(key=client_key, enabled=True).rsa
        except models.Consumer.DoesNotExist:
            return settings.LTI_DUMMY_RSA

    def validate_client_key(self, client_key, request):
        try:
            models.Consumer.objects.get(key=client_key)
        except models.Consumer.DoesNotExist:
            return False
        return True

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request, request_token=None, access_token=None):
        try:
            dt = datetime.utcfromtimestamp(int(timestamp)) - datetime.utcnow()
            if abs(dt.total_seconds()) > settings.LTI_NONCE_TIMEDELTA_MAX:
                logger.warn(f'Possible replay attack detected: {client_key}')
                return False
        except ValueError:
            logger.debug(f'Could not convert to int: {timestamp}')
            return False
        token = request_token or access_token
        key = f'lti-replay-{client_key}-{timestamp}-{nonce}-{token}'
        if cache.get(key, None):
            return False
        cache.set(key, True, timeout=settings.LTI_NONCE_TIMEDELTA_MAX * 2)
        return True
