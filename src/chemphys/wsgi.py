import os
import sys


sys.path.insert(0, '/www/chemphys/chemphys/src')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chemphys.settings")


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
