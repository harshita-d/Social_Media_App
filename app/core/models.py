"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """user model manager"""

    # manager is associated to a model, so need a way to access the model which the manager is associated with for this we use self.model which is same as defining a new user
    def create_user(self, email, password=None, **extraFields):
        """create->save->return new user"""
        # Create

        # condition to check empty email address
        if not email:
            raise ValueError("User must have an email address")
        # self.normalize is provided by BaseUserManager to normalize email
        user = self.model(email=self.normalize_email(email), **extraFields)
        user.set_password(password)  # here it will encrypt the password

        # Save
        user.save(using=self._db)  # here self._db is usd to save multiple databases

        # return
        return user

    def create_superuser(self, email, password):
        """create, save and return a new superuser"""

        # create
        # for creating a user we can make use of above method of create_user
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        # save
        user.save(using=self._db)

        # return
        return user


# AbstractBaseUser contains the functionality for the authentication system
# PermissionMixin contains the functionality for the permissions and fields
class User(AbstractBaseUser, PermissionsMixin):
    """Existing User"""

    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # this creates an instance of usermanager class

    USERNAME_FIELD = "email"
