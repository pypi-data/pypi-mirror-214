"""
Copyright (c) 2014-present, aglean Inc.
"""
import pytest
from django.conf import settings


def pytest_configure():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'anorganization'
        ],
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory',
            }
        }
    )
