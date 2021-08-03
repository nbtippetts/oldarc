"""
Django settings for arc project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'if&(y*+3iya!ix#)xh=ycq5y&8i36@exr&kkl_og2_7$(##u(q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = ['*', '172.21.0.2', '172.21.0.1','174.52.250.10', 'arc.dev', 'arc', '192.168.1.18', '172.18.0.1', 'web', '0.0.0.0', 'localhost', '127.0.0.1', 'redis', '[::1]']


# Application definition
INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'humidity.apps.HumidityConfig',
    'schedule.apps.ScheduleConfig',
    'streamapp.apps.StreamappConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'django_forms_bootstrap',
    'bootstrap_datepicker_plus',
    'chartjs',
    'jquery'
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

ROOT_URLCONF = 'arc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'libraries':{
                'schedule_display': 'schedule.templatetags.schedule_display',
                'humidity_display': 'humidity.templatetags.humidity_display',
            },
        },
    },
]

WSGI_APPLICATION = 'arc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'arc_db',
        'USER': 'pi',
        'PASSWORD': 'rnautomations',
        'HOST': 'db',
        # 'HOST': 'localhost',
        'PORT': 5432,
    }
}

BOOTSTRAP4 = {
    'include_jquery': True,
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/



STATIC_URL='/static/'
# as declared in NginX conf, it must match /opt/services/djangoapp/static/
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# do the same for media files, it must match /opt/services/djangoapp/media/
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'media')

LOGIN_REDIRECT_URL='homepage'
LOGIN_URL='login'
EMAIL_BACKED='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='stmp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='nbtippetts@gmail.com'
EMAIL_HOST_PASSWORD='wicked2007'