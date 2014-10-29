"""
WSGI config for chemphys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
sys.path.insert(0, '/www/chemphys/chemphys/src')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chemphys.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
