import datetime
import facebook

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings

from chores.models import House
from chores.sms import SMSClient

today = datetime.datetime.now().strftime('%A').lower()

class Command(BaseCommand):
  help = 'Runs daily stuff'

  def handle(self, *args, **options):
    for house in House.objects.filter(recurs__iexact=today):
      print 'Entering: %s' % house.name

      for chore in house.chores.all():
        print 'Chore: %s' % chore.name
        if chore.user and chore.user.confirmed:
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

          if settings.DEBUG == True:
            print SMS_MSG % (chore.user.name, chore.name)
          else:
            client = SMSClient(chore.user)
            client.send_message(SMS_MSG % (chore.user.name, chore.name))

      house.shuffle()
