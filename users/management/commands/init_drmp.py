import os
from django.core.management.base import BaseCommand
import logging
from users.management.commands.utils.init_apps import init_apps
from users.management.commands.utils.init_users import init_users
from users.management.commands.utils.init_permissions import init_permission
from users.management.commands.utils.init_departments import init_department
from users.management.commands.utils.init_roles import init_role
from users.management.commands.utils.init_member import init_member
from users.management.commands.utils.init_models import init_models
from users.management.commands.utils.init_dmp import init_dmp
from users.management.commands.utils.init_drp import init_drp

PROJECT_PATH = os.path.abspath(".")
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('app', type=int)

    def handle(self, *args, **options):
        print(options['app'])
        logger.info("Initializing apps data!")
        init_apps(options["app"])
        logger.info("Initializing users data!")
        init_users(options["app"])
        logger.info("Initializing permission data!")
        init_permission(options["app"])
        logger.info("Initializing department data!")
        init_department(options["app"])
        logger.info("Initializing roles data!")
        init_role(options["app"])
        logger.info("Initializing member data!")
        init_member(options["app"])
        logger.info("Initializing models data!")
        init_models(options["app"])
        logger.info("Initializing department model permission data!")
        init_dmp(options["app"])
        logger.info("Initializing department role model permission data!")
        init_drp(options["app"])
