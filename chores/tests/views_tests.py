from django.test import TestCase
from chores import views
import json
import facebook
import smtplib

from django import http
from django.conf import settings
from django.contrib.auth import models as auth_models, login, logout, authenticate
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from chores.models import User, House, Chore
from chores.utils import Facebook, untokenize
from chores.context import context
from chores.users.invitations import Invitation

class ViewTest(TestCase):
  fixtures = ['chores_views_testdata.json']

  def test_index(self):
    resp = self.client.get(reverse('index'))
    self.assertEqual(resp.status_code, 200)
    
  def test_login_view(self):
    resp = self.client.get(reverse('login'))
    self.assertEqual(resp.status_code, 200)

  def test_api_house(self):
    resp = self.client.get(reverse('api_house'))
    self.assertEqual(resp.status_code, 200)
    self.assertTrue('butt' in resp.context)