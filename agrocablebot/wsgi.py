"""
WSGI config for agrocablebot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrocablebot.settings')

application = get_wsgi_application()

from mqtt.mqtt import MQTT_CLIENT

MQTT_CLIENT.client.loop_start()