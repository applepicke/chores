from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse

from chores.utils import tokenize
from chores.models import User, House, Chore
from chores.messages import CONFIRMATION_MSG, INVITATION_MSG

# Confirmation email when being invited to a household
class Invitation(object):

  def __init__(self, member_request, house, domain):
    self.member_request = member_request
    self.house = house
    self.domain = domain

  def generate_confirmation_link(self):
    token = tokenize(str(self.member_request.id))
    url = reverse('confirmation', args=(token,))
    return 'http://%s%s' % (self.domain, url)

  def send(self):
    send_mail(
      'Chores Invitation',
      INVITATION_MSG % {
        'owner': self.house.owner.name,
        'household': self.house.name,
        'confirmation_link': self.generate_confirmation_link(),
      },
      settings.CHORES_FROM_EMAIL,
      [self.member_request.user.email],
      fail_silently=False
    )

# Original email confirmation when signing up
class Confirmation(object):

  def __init__(self, user, domain):
    self.user = user
    self.domain = domain

  def generate_confirmation_link(self):
    token = tokenize(self.user.get_confirmation_token())
    url = reverse('confirm_email', args=(token,))
    return 'http://%s%s' % (self.domain, url)

  def send(self):
    send_mail(
      'Welcome to Chores',
      CONFIRMATION_MSG % {
        'user': self.user.full_name,
        'confirmation_link': self.generate_confirmation_link(),
      },
      settings.CHORES_FROM_EMAIL,
      [self.user.email],
      fail_silently=False
    )


