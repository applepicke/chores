import datetime
import facebook

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from chores.models import House

today = datetime.datetime.now().strftime('%A').lower()
today = 'sunday'

msg = """
Your chore is: %s
Description: %s

Love,
Willy
"""

class Command(BaseCommand):
  help = 'Makes mockdata'

  def handle(self, *args, **options):
    for house in House.objects.filter(recurs__iexact=today):
      for chore in house.chores.all():
        if chore.user:
          graph = facebook.GraphAPI(chore.user.access_token)
          email = graph.get_object('me').get('email')
          if email:
            send_mail(
              'Chores',
              msg % (chore.name, chore.description),
              'wcurtiscollins@gmail.com',
              [email],
              fail_silently=False
            )
            print 'sending mail to %s' % email
