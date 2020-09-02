"""
Django settings for report project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import pathlib
import structlog

from django.utils.translation import gettext_lazy as _

from os2datascanner.projects.django_toml_configuration import process_toml_conf_for_django

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(pathlib.Path(
    __file__).resolve().parent.parent.parent.parent.absolute())
PROJECT_DIR = os.path.dirname(BASE_DIR)

process_toml_conf_for_django(
    parent_path=PROJECT_DIR,
    module=sys.modules[__name__],
    sys_var='DSC_REPORT_SYSTEM_CONFIG_PATH',
    user_var='DSC_REPORT_USER_CONFIG_PATH',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': globals()['DEBUG'],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        ),
    },
]

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        "gelf": {
            "()": "os2datascanner.utils.gelf.GELFFormatter",
        },
        "json": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": structlog.processors.JSONRenderer(),
        },
        "console": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": structlog.processors.KeyValueRenderer(key_order=[
                'timestamp',
                'level',
                'event',
                'logger',
            ]),
        },
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s'
            ),
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        "requires_graylog_host": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: bool(globals()['GRAYLOG_HOST']),
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            'filters': ['require_debug_true'],
            "formatter": "console",
        },
        "debug_log": {
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": globals()['VAR_DIR'] + '/debug.log',
            'filters': ['require_debug_true'],
            "formatter": "key_value",
        },
        "graylog": {
            "level": "DEBUG",
            "class": "os2datascanner.utils.gelf.GraylogDatagramHandler",
            "host": globals()['GRAYLOG_HOST'],
            "filters": ["requires_graylog_host"],
            "formatter": "gelf",
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_structlog': {
            'handlers': ['console', 'debug_log', 'graylog'],
            'level': globals()['DJANGO_LOG_LEVEL'],
            'propagate': True,
        },
        'os2datascanner': {
            'handlers': ['console', 'debug_log', 'graylog'],
            'level': globals()['DJANGO_LOG_LEVEL'],
            'propagate': True,
        },
    }
}

