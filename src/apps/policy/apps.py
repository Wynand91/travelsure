from os import path, makedirs

from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.policy'
    verbose_name = 'Policies'