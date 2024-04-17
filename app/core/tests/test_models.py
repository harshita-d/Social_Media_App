"""
Tests for models0
"""

from django.test import TestCase  # TestCase is a base class for our Test
from django.contrib.auth import get_user_model

# get_user_model is a helper function provided by django to get default user model for the project # noqa: E501
# Using get_user_model() allows your code to adapt to changes in the user model without modifications. # noqa: E501
# If you switch to a different custom user model, you only need to update the AUTH_USER_MODEL setting. # noqa: E501


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """test creating an user with email successful"""
        email = "test@example.com"
        password = "123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        # create a new user instance and perform assertions to validate the creation process. # noqa: E501
        # get_user_model().objects accesses the default manager (typically objects) of the retrieved user model # noqa: E501
        # The create_user() method is called on the user model's default manager (objects) to create a new user instance with the specified email and password. # noqa: E501

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        # self.assertEqual(user.email, email): Asserts that the email attribute of the created user instance matches the provided email. # noqa: E501
        # self.assertTrue(user.check_password(password)): Asserts that the check_password() method returns True when validating the provided password against the hashed password stored in the user instance. # noqa: E501

    def test_new_user_email_normalize(self):
        """test email is normalized for new users by lowercasing the second part of email i.e is after @"""
        # in below sample first part is the input email from user and second is the normalized email. # noqa: E501
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["test3@EXAMPLE.COM", "test3@example.com"],
            ["Test4@example.cOm", "Test4@example.com"],
        ]

        for email, expected in sample_emails:
            # here get_user_model is a default user model
            # create_user is the function in UserManager which is associated with custom user model class User # noqa: E501
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)
