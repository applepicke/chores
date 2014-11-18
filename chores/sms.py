from django.conf import settings

from twilio.rest import TwilioRestClient

from chores.cache import cache
from chores.utils import random_string

client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

VERIFICATION_MSG = "Chores SMS verification code: %s"

class SMSClient(object):

  def __init__(self, user):
    self.user = user

  def send_verification_code(self, code, number):
    if settings.DEBUG:
      print VERIFICATION_MSG % code
    else:
      client.messages.create(
        to=number,
        from_=settings.TWILIO_NUM,
        body=VERIFICATION_MSG % code,
      )

  def send_message(self, message):
    if self.user.can_receive_sms:
      if settings.DEBUG:
        print message
      else:
        client.messages.create(
          to=self.user.phone_number,
          from_=settings.TWILIO_NUM,
          body=message,
        )



