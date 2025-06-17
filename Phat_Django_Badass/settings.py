import os
from dotenv import load_dotenv
from pathlib import Path
from settings.installed_apps import *
from settings.middlewares import *
from settings.general import *
from settings.rest_framework import *
from settings.sessions import *
from settings.databases import *
from settings.humanizers import *
from settings.security import *

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY
DEBUG

# General -> settings/general.py
INSTALLED_APPS
MIDDLEWARE
ROOT_URLCONF
WSGI_APPLICATION
DEFAULT_AUTO_FIELD
APPEND_SLASH
DJANGO_ADMIN_LOGS_ENABLED
X_FRAME_OPTIONS
STATIC_URL
STATIC_ROOT
STATICFILES_STORAGE
TEMPLATES

# Security -> settings/security.py
ALLOWED_HOSTS
CORS_ALLOW_ALL_ORIGINS
AUTH_PASSWORD_VALIDATORS

# Django REST Framework -> settings/rest_framework.py
REST_FRAMEWORK

#Databases -> settings/databases.py
DATABASES

# Humanizing -> settings/humanizers.py
LANGUAGE_CODE
TIME_ZONE
USE_I18N
USE_TZ
USE_THOUSAND_SEPARATOR
USE_L10N

# Session settings -> settings/sessions.py
SESSION_EXPIRE_SECONDS
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD
SESSION_EXPIRE_AFTER_LAST_ACTIVITY
SESSION_EXPIRE_AT_BROWSER_CLOSE
SESSION_TIMEOUT_REDIRECT