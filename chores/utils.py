import urllib2
import json
import logging
import base64
import random
import string
import pytz

from django.conf import settings

logger = logging.getLogger('')

def random_string(size=5, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def rando_msg(msgs):
  num = random.randint(0, len(msgs) - 1)
  return msgs[num]

def tokenize(txt):
  return base64.urlsafe_b64encode('%s:%s' % (txt, settings.SECRET))

def untokenize(token):
  txt, secret = base64.urlsafe_b64decode(str(token)).split(':')
  return txt

def to_utc(datetime, user):
  tz = pytz.timezone(user.timezone or 'UTC')
  return tz.localize(datetime, is_dst=None).astimezone(pytz.utc)

def from_utc(datetime, user):
  tz = pytz.timezone(user.timezone or 'UTC')
  return datetime.astimezone(tz).replace(tzinfo=None)

class Facebook(object):
  user_info = None

  def __init__(self):
    self.user_info = None

  @staticmethod
  def get_access_token():
    try:
      return urllib2.urlopen("https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials" % (
        settings.APP_ID,
        settings.APP_SECRET,
      )).read().split('=')[1]
    except urllib2.HTTPError, e:
      logger.error('HTTPError = ' + str(e.code))
      logger.error(e.read())


  def get_user_info(self, user_id):
    response = urllib2.urlopen("https://graph.facebook.com/user/%s?access_token=%s" % (
      user_id,
      self.get_access_token(),
    )).read()

    self.user = json.loads(response).get('data')

    return self.user


  def check_user(self, input_token, user_id):
    try:
      response = urllib2.urlopen("https://graph.facebook.com/debug_token?access_token=%s&input_token=%s" % (
        self.get_access_token(),
        input_token
      )).read()
    except urllib2.HTTPError, e:
      logger.error('HTTPError = ' + str(e.code))
      logger.error(e.read())

    self.user_info = json.loads(response).get('data')

    if self.user_info.get('app_id') != '%s' % settings.APP_ID:
      return False

    if self.user_info.get('user_id') != '%s' % user_id:
      return False

    return self.user_info.get('is_valid')
