import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-27vrxw&o^o5^imb39j!dpv$ivvw&ijmq%k^9)$#@=e_l2o(-vq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['staff-tracker.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'staff_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tracker/templates')],  # Ensure this points to your templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'staff_tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'contract_db', # Your database name
#         'USER': 'root', # Your MySQL user
#         'PASSWORD': 'Breakingbenjamnins01@', # Your MySQL password
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# BASE_DIR should be correctly defined
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
#
# # Ensure Django knows where to find static files
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'tracker/static'),
# ]
# # For production: where collected static files are stored
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ensure you have a 'static' folder in your Django project
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Use WhiteNoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')



# ✅ Media Files (Uploaded Files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = 'dashboard'  # Admins go to dashboard
LOGOUT_REDIRECT_URL = 'home'  # Redirect to homepage after logout

LOGIN_REDIRECT_URL = 'home'  # This ensures the home view handles the redirect logic


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True  # Enable SSL
EMAIL_HOST_USER = 'tyaji247@gmail.com'
EMAIL_HOST_PASSWORD = 'enip jvva jita ufaj'  # Use a 16-character Gmail App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
