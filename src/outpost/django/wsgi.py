"""
WSGI config for Outpost project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.abspath(os.path.join(__file__, '../../..')))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outpost.app.settings')

application = get_wsgi_application()
