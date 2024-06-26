from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

# The APIClient class from Django Rest Framework's test module is used for testing API endpoints in Django applications.
# It allows you to make requests to your API endpoints directly from your test code, without needing to run a server.

from rest_framework import status


CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "test@example.com",
            "password": "123",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # checking if API response is 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # checking in API if the email sending in payload is equal to the email we are getting in response
        # this will retrieve object from DB with sending email through which we created account
        user = get_user_model().objects.get(email=payload["email"])

        # the below line checks if the password we are getting in object is same as we send in payload
        self.assertTrue(user.check_password(payload["password"]))

        # here we are checking that the saved password is not returned in response as it can cause a security issue
        self.assertNotIn("password", res.data)

    def test_user_with_email_exist_error(self):
        payload = {
            "email": "test@example.com",
            "password": "123",
            "name": "Test Name",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            "email": "test@example.com",
            "password": "123",
            "name": "Test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # below lines will check if user exists or not after getting 400 bad request status
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)
