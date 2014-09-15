from django.test import TestCase
from model_mommy import mommy
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib import admin

from jsonfield import JSONField

from chores import models


class ModelTest(TestCase):

  def test_User(self):
    # Setup test
    new_user = mommy.make('chores.User')
    self.assertTrue(isinstance(new_user,models.User))

    # Test if has password
    self.assertFalse(new_user.d_user)

    # Test Name confirmation
    self.assertEqual(new_user.name, new_user.email + ' (Pending)')
    new_user.confirmed = True
    self.assertEqual(new_user.name, new_user.first_name + ' ' + new_user.last_name)

    # Test the houses the user belongs to
    self.assertFalse(new_user.house)
    new_house = mommy.make('chores.House', owner = new_user)
    self.assertEqual(new_user.house, new_house)