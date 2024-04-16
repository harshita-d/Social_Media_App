"""
Test custom Django management commands.
"""

from unittest.mock import patch  # noqa

from psycopg2 import OperationalError as Psycopg2Error  # noqa
from django.core.management import call_command  # noqa
from django.db.utils import OperationalError  # noqa
from django.test import SimpleTestCase  # noqa


@patch("core.management.commands.wait_for_db.Command.check")  # noqa
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database ready if the database is ready"""
        # One possible test case: run wait_for_db command, and the DB is already ready. # noqa: E501
        # In this case, we can execute our application, and no need to do anything. # noqa: E501

        patched_check.return_value = True  # noqa
        # The above line indicates that when the `check` method of the wait_for_db command is called during the test execution, it will return True. # noqa: E501

        call_command("wait_for_db")
        # Call the management command function or use call_command if necessary. # noqa: E501
        # This line executes the code in wait_for_db in a situation where the database is ready and we run the command. # noqa: E501
        # Also checks if the command is set up correctly. # noqa

        patched_check.assert_called_once_with(databases=["default"])  # noqa
        # This assertion verifies that during the execution of `call_command('wait_for_db')`, # noqa: E501
        # the `check` method was called exactly once with the argument `database=['default']`. # noqa: E501
        # Placing the assertion call after call_command ensures that the command is executed and then verify that within the execution of that command, # noqa: E501
        # a specific method 'check' was called as expected. # noqa

    @patch("time.sleep")  # noqa
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """If the database is not ready"""
        """Test waiting for the database when getting OperationalError"""
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )  # noqa

        # The first two calls to patched_check will raise Psycopg2Error (this error occurs when the database is not ready to make a connection). # noqa: E501
        # The next three calls will raise OperationalError (this error occurs when the database is ready to make connections but hasn't set up the testing database). # noqa: E501
        # The subsequent call will return True.

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)  # noqa
        # Assertion checks whether the call_count attribute of the patched_check mock object is equal to 6. # noqa: E501
        # This is commonly used to verify how many times a particular function or method has been called during the execution of a test. # noqa: E501
        # This assertion is ensuring that our code is interacting with the patched_check as expected during the test, making the specified number of calls. # noqa: E501
        # If the call count is not 6, the test will fail.

        patched_check.assert_called_with(databases=["default"])  # noqa
        # This assertion is checking whether the patched_check mock object was called at least once with the specified arguments. # noqa: E501
        # Here it's checking that the 'database' argument passed to the patched_check during any of its calls is equal to ['default']. # noqa: E501
        # If the mock has been called with different arguments or has not been called, the assertion will fail. # noqa: E501

        # patched_sleep is a mock object that is standing in for the time.sleep function. # noqa: E501
        # It helps to simulate different time-related scenarios without actually waiting for a real-time interval. # noqa: E501


# noqa
