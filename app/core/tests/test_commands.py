"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class  CommandTests(SimpleTestCase):
    """Test commands."""
    #It replaces the real Command.check method with a mock object as the patched_check argument.
    def test_wait_for_db_ready(self, patched_check):
        """ whenever the code calls Command.check(), it will return True rather than actually performing any real database check."""
        patched_check.return_value = True

        call_command('wait_for_db')
        #If the command had never called check(), the test would fail. Similarly, if it called check() with the wrong arguments, the test would also fail.
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]
        print(patched_check.call_count)
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
