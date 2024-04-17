""""
Django command to wait for database to be available
"""

from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        self.stdout.write("waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("database unavailable, waiting 1 second")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available"))


# the command inherit from the basecommand, which is the base class for all management commands in Django.
# the handle method is the entry point for the management command. it is called when the command is executed.
