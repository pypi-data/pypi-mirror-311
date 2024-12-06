import logging
from os import environ

log = logging.getLogger(__name__)

ANTHROPIC_API_KEY = environ.get('ANTHROPIC_API_KEY', None)
