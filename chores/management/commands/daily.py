import datetime
import facebook

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings

from chores.models import House

from twilio.rest import TwilioRestClient

today = datetime.datetime.now().strftime('%A').lower()

EMAIL_MSG = """
Your chore is: %s
Description: %s

Love,
Willy
"""

SMS_MSG = """
Hello %s, your chore for the week is %s.
"""

class Command(BaseCommand):
  help = 'Makes mockdata'

  def handle(self, *args, **options):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    for house in House.objects.filter(recurs__iexact=today):
      print 'Entering: %s' % house.name

      for chore in house.chores.all():
        print 'Chore: %s' % chore.name
        if chore.user:
          email = chore.user.email

          if email:
            send_mail(
              'Chores',
              EMAIL_MSG % (chore.name, chore.description),
              'wcurtiscollins@willyc.me',
              [email],
              fail_silently=False
            )
            print 'sending mail to %s' % email

          number = chore.user.phone_number

          if settings.DEBUG == True:
            print SMS_MSG % (chore.user.name, chore.name)
          elif number:
            client.messages.create(
              to=number,
              from_=settings.TWILIO_NUM,
              body=SMS_MSG % (chore.user.name, chore.name)
            )

      house.shuffle()
