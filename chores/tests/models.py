from model_mommy import mommy

from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib import admin

from chores import models
from chores.tests.base import ChoresTestCase

class ModelTest(ChoresTestCase):

  def test_User(self):
    # Setup test
    new_user = mommy.make('chores.User', email='test@weiner.com')
    self.assertTrue(isinstance(new_user,models.User))

    # Test if has password
    self.assertFalse(new_user.has_password)
    new_d_user = auth_models.User.objects.create(email=new_user.email, username=new_user.email)
    new_user.d_user = new_d_user
    new_d_user.set_password('abc123')
    self.assertTrue(new_user.has_password)
    new_d_user.set_unusable_password()
    self.assertFalse(new_user.has_password)

    # Test Name confirmation
    self.assertEqual(new_user.name, new_user.email + ' (Pending)')
    new_user.confirmed = True
    self.assertEqual(new_user.name, new_user.first_name + ' ' + new_user.last_name)

    # Test the houses the user belongs to
    self.assertFalse(new_user.house)
    new_house = mommy.make('chores.House', owner=new_user)
    self.assertEqual(new_user.house, new_house)

    # Test the chores that belong to the user
    self.assertListEqual(list(new_user.chores.all()), [])
    new_chore_1 = mommy.make('chores.Chore', users=[new_user], house=new_house)
    new_chore_2 = mommy.make('chores.Chore', users=[new_user], house=new_house)
    self.assertListEqual(list(new_user.chores.all()), [new_chore_1, new_chore_2])

    # Test the add_d_user method
    new_user_2 = mommy.make('chores.User', email='test-2@weiner.com')
    new_user_2.add_d_user(email=new_user_2.email)
    self.assertEqual(new_user_2.email, new_user_2.d_user.email)
    new_user_2.add_d_user(email=new_user_2.email)
    self.assertEqual(new_user_2.email, new_user_2.d_user.email)

    #Test the owns_chore method
    self.assertFalse(new_user_2.owns_chore(new_chore_1.id))
    self.assertTrue(new_user.owns_chore(new_chore_1.id))

    #Test as_dict method
    new_user_dictionary = new_user.as_dict()
    self.assertEqual(new_user.id, new_user_dictionary['id'])
    self.assertEqual(new_user.name, new_user_dictionary['name'])
    self.assertEqual(new_user.first_name, new_user_dictionary['first_name'])
    self.assertEqual(new_user.last_name, new_user_dictionary['last_name'])
    self.assertEqual(new_user.email, new_user_dictionary['email'])
    self.assertEqual(new_user.confirmed, new_user_dictionary['confirmed'])
    self.assertEqual(new_user.has_password, new_user_dictionary['has_password'])
    self.assertEqual(new_user.email_enabled, new_user_dictionary['email_enabled'])
    self.assertEqual(new_user.sms_enabled, new_user_dictionary['sms_enabled'])
    self.assertEqual(new_user.sms_verified, new_user_dictionary['sms_verified'])

    #Test the represent as string method
    self.assertEqual(new_user.name, str(new_user))

  def test_house(self):
    #Setup test and test house model
    new_house = mommy.make('chores.House')

  def test_house_rotation(self):
    self.house.shuffle()

    chores = self.house.chores.order_by('id')

    self.assertEqual(chores[0].user, self.user3)
    self.assertEqual(chores[1].user, self.user)
    self.assertEqual(chores[2].user, self.user2)

    self.house.shuffle()

    chores = self.house.chores.order_by('id')

    self.assertEqual(chores[0].user, self.user2)
    self.assertEqual(chores[1].user, self.user3)
    self.assertEqual(chores[2].user, self.user)

