"""
WSGI config for agrocablebot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["MARIADB_USER"]="imacuna"
os.environ["MARIADB_PASSWORD"]="pi"
os.environ["MARIADB_HOST"]="127.0.0.1"
os.environ["MARIADB_PORT"]="3306"
os.environ["MQTT_BROKER_USERNAME"]="imacuna"
os.environ["MQTT_BROKER_PASSWORD"]="pi"
os.environ["MQTT_BROKER_HOST"]="127.0.0.1"
os.environ["MQTT_BROKER_PORT"]="1883"

os.environ["ABOVE_CAMERA"]="Droidcam"
os.environ["BELOW_CAMERA"]="EasyCamera"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrocablebot.settings')

application = get_wsgi_application()
