from django.test import TestCase
from django.core.urlresolvers import reverse

class ViewTest(TestCase):

  def test_index(self):
    resp = self.client.get(reverse('index'))
    self.assertEqual(resp.status_code, 200)

  def test_login_view(self):
    resp = self.client.get(reverse('login'))
    self.assertEqual(resp.status_code, 200)

# def test_api_house(self):
#   resp = self.client.get(reverse('api_house'))
#   self.assertEqual(resp.status_code, 200)
#   self.assertTrue('butt' in resp.context)