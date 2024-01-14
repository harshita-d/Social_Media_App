"""
test custom Django management commands.
"""
from unittest.mock import patch
# patch function is commonly used in unit testing to temporarily modify objects functions  
# or classes to isolate specific functionality for testing without affecting the actual implementation 

from psycopg2 import OperationalError as Psycopg2Error
# OperatonalError is typically raised when there's an issue during the execution of database operations. 

from django.core.management import call_command
# call_commands allows us to trigger built in or custom custom Django commands from scripts or other parts of django application

from django.db.utils import OperationalError
# OperationalError from djnago is raised when there's a problem executing database queries 
# or when database is unavailable or misconfigured 

from django.test import SimpleTestCase
# Its a base class provided by django for creating a simple testcases

@patch('core.management.commands.wait_for_db.Command.check')
# In the above command we are trying to mock the 'check' method within the wait_for_db command from the core app in Django project.
# @patch is a decorator which will replace the check method within the wait_for_db command class
#  

class CommandTests(SimpleTestCase):
    """Test commands"""
    def test_wait_for_db_ready(self, patched_check):
        """test waiting for database ready if database is ready"""
        # here one possible testcase can be we run wait_for_db command and DB is already ready
        # so in this case we can execute our application and no need to do anything
        
        patched_check.return_value=True
        # the above line indicates that when the `check` method of the wait_for_db command is called during the test execution it will return True
        
        call_command('wait_for_db')
        # call the management command function or use call_command if necessary
        # this line executes the code in wait_for_db means the situation where database is ready and we run the command 
        # also checks if the command is set up correctly

        patched_check.assert_called_once_with(database=['default'])
        # This assertion verifies that during the execution of `call_command('wait_for_db')` the `check` method was called exactly once with the argument `database=['default']`
        # placing the assertion call after call_command ensures that the command is executed and then verify that within the execution of that command a specific method 'check' was called as expected.

    @patch('time.sleep')    
    # the argument which is declared near to the function should be defined once like for @patch('time') is declared near to function call therefore its written first then the @patch("check") as its written farther away
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """if the database is not ready"""
        """test waiting for database when getting operationalError"""
        patched_check.side_effect=[Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        
        # patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]:- 
        #         The first two calls to patched_check will raise Psycopg2Error(this error occurs when the database is not ready to make connection).
        #         The next three calls will raise OperationalError. (this error occurs when database is ready to make connections but hasn;t setup the testing database)
        #         The subsequent call will return True.

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count,6)
        # assertion is checking whether the call_count attribute of the patched_check mock object is equal to 6.
        # this is commonly used to verify how many times a particular function or method has been called during the execution of a test.
        # this assertion is ensuring that our code is interacting with the patched_check as expected during the test, making the specified number of calls,
        # if the call count is not 6, the test will fail.

        patched_check.assert_called_with(database=['default']) 
        # this assertion is checking whether the patched_check mock object was called atleast once with the specified arguments.
        # here its checking that the 'database' argument passed to the patched_check during any of its callis equal to ['default'] 
        # if the mock has been called with the different arguments or has not been called the assertion will fail.

        # patched_sleep is a mock object that is standing in for the time.sleep function 
        # it helps to simulate different time related scenarios without actually waiting for real time interval. 