"""
WSGI config for openservices project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outpost.settings')

application = get_wsgi_application()
