import urllib2
import json
import logging
import base64
import random
import string
import pytz
import urllib
import hashlib
import datetime

from django.conf import settings
from django.core.mail import mail_admins

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

def to_utc(time, user=None):
  timezone = user.timezone if user else 'UTC'
  tz = pytz.timezone(timezone or 'UTC')
  return tz.localize(time, is_dst=None).astimezone(pytz.utc)

def from_utc(time, user=None):
  timezone = user.timezone if user else 'UTC'
  tz = pytz.timezone(timezone or 'UTC')
  return time.astimezone(tz)

def user_time(time, user, full_date=False):
  now = datetime.datetime.now()

  if isinstance(time, basestring):
    time = datetime.datetime.strptime(time, '%I:%M %p')

  time = time.replace(year=now.year, month = now.month, day=now.day)
  time = to_utc(time)


  format = '%I:%M %p'

  if full_date:
    format = '%I:%M %p %B %d, %Y'

  return from_utc(time, user).strftime(format)

def gravatar(email, size=25):
  gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
  gravatar_url += urllib.urlencode({'s':str(size)})

  return gravatar_url

def errorize(e, type):
  import traceback

  subject = '%s' % type
  msg = '%s: %s\n\n%s' % (type, e, traceback.format_exc())

  logger.debug(msg)
  mail_admins(subject, msg)

def get_timezones():
  NOW = datetime.datetime.now()
  ZERO = datetime.timedelta(0)

  timezones = {}

  for tname in pytz.common_timezones:
    tzone = pytz.timezone(tname)
    std_date = None
    try:
      for utcdate, info in zip(tzone._utc_transition_times, tzone._transition_info):
        utcoffset, dstoffset, tzname = info
        if dstoffset == ZERO:
          std_date = utcdate
        if utcdate > NOW:
          break
    except AttributeError:
      std_date = NOW

    std_date = tzone.localize(std_date)
    timezones[tname] = {
      'label': '(UTC{z}) {n}'.format(n=tname, z=std_date.strftime('%z')),
      'key': tname,
    }
  return timezones
