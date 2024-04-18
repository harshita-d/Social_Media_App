"""tests for Django admin modifications"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

# Client is a django test client that is used make http request


class AdminSiteTests(TestCase):
    """Test for Django Admin"""

    # the "setUp" should be like this as its a default test name that will run before every test
    def setUp(self):
        """create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="123",
        )

        # force login allows to make an HTTP request authenticated
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="123",
            name="Test USer",
        )

    def test_user_list(self):
        """tests that users are listed on the page"""

        # when admin site is deployed, the views provided by that site are accessible using Django URL reversing system
        # reverse is use to get the url for changelist inside Django app
        # admin:core_user_changelist is a syntax to determines which url we will pull
        # changelist is a page of list of users
        url = reverse("admin:core_user_changelist")

        # self.client.get makes HTTP request
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """test the edit user page works"""

        # the url core_user_change is for the change user page and we need to pass specific id for the user we want to change
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test the create user page works"""

        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
