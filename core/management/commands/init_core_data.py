import os
from django.core.management.base import BaseCommand
import logging
from core.management.commands.utils.init_country import init_country
from core.management.commands.utils.init_modules import init_modules

PROJECT_PATH = os.path.abspath(".")
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Initializing country data!")
        init_country()
        logger.info("Initializing modules data!")
        init_modules()
