import urllib2
import json

from django.conf import settings

class Facebook(object):
  user_info = None

  def __init__(self):
    response = urllib2.urlopen("https://graph.facebook.com/debug_token?access_token=%s&input_token=%s" % (
      self.get_access_token(),
      input_token
    )).read()

    self.user_info = json.parse(response)

  @staticmethod
  def get_access_token(self):
    return urllib2.urlopen("https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials" % (
      settings.APP_ID,
      settings.APP_SECRET,
    )).read().split('=')[1]

  def check_user(self, input_token, user_id):
    if self.user_info.get('app_id') != settings.APP_ID:
      return False

    if self.user_info.get('user_id') != user_id:
      return False

    return self.user_info.get('is_valid')
