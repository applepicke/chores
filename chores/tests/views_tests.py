from django.test import TestCase

class BasicTest(TestCase):

  def test_index(self):
    resp = self.client.get('/')
    self.assertEqual(resp.status_code, 200)
    