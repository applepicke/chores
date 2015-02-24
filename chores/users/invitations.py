from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse

from chores.utils import tokenize
from chores.models import User, House, Chore

INVITATION_MSG = """
Hello,

%(owner)s has invited you to join the %(household)s household.
Don't be embarrassed, it's probably just because you're a big slob. We all have our faults.

To confirm your role in the household, click on the following link:
%(confirmation_link)s

If you think you might have gotten this email by mistake, then someone is probably playing a huge prank on you. Hilarious.

love,
The Chore People

"""

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
      'wcurtiscollins@willyc.me',
      [self.member_request.user.email],
      fail_silently=False
    )

