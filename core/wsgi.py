import os
from django.core.wsgi import get_wsgi_application

# On définit les réglages avant toute chose
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialisation de l'application
application = get_wsgi_application()