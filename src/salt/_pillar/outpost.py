# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

import logging
import re

from salt.ext import six

logger = logging.getLogger(__name__)

grain_pattern = re.compile(r'<(?P<grain_name>.*?)>')
try:
    import requests
    from requests.exceptions import RequestException
    from salt.ext.six.moves.urllib.parse import quote as _quote
    _HAS_DEPENDENCIES = True
except ImportError:
    _HAS_DEPENDENCIES = False


def __virtual__():
    return _HAS_DEPENDENCIES


def ext_pillar(minion_id,
               pillar,  # pylint: disable=W0613
               url,
               username=None,
               password=None,
               with_grains=False):
    url = url.replace('%s', _quote(minion_id))
    if with_grains:
        # Get the value of the grain and substitute each grain
        # name for the url-encoded version of its grain value.
        for match in re.finditer(grain_pattern, url):
            grain_name = match.group('grain_name')
            grain_value = __salt__['grains.get'](grain_name, None)

            if not grain_value:
                logger.error(
                    "Unable to get minion '%s' grain: %s",
                    minion_id,
                    grain_name
                )
                return {}

            grain_value = _quote(six.text_type(grain_value))
            url = re.sub('<{0}>'.format(grain_name), grain_value, url)
    try:
        r = requests.get(url, auth=(username, password))
        r.raise_for_status()
    except RequestException as e:
        logger.warning(e)
    else:
        return r.json()
