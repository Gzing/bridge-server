# -*- coding: utf-8 -*-
"""Test configs."""
from app.app_config import AppConfig
from util.tasks import CeleryConfig
from config import settings


def test_app_config():
    assert AppConfig.SQLALCHEMY_DATABASE_URI is not None


def test_celery_config():
    assert CeleryConfig.SQLALCHEMY_DATABASE_URI is not None
    assert settings.REDIS_URL is not None
