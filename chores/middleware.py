import json

from django import http
from django.core.urlresolvers import reverse

from chores.models import User

class UserMiddleware(object):
  def process_request(self, request):

    try:
      if request.user.is_authenticated():
        request.app_user = User.objects.filter(d_user__id=request.user.id).latest('id')
      else:
        request.app_user = None
    except:
      request.app_user = None

    return None

class JSONMiddleware(object):
  def process_request(self, request):
    try:
      data = json.loads(request.body)
    except:
      data = {}

    temp = request.POST.dict()
    temp.update(data)
    request.POST = temp

    return None

class ConfirmationMiddleware(object):
  def process_request(self, request):
    path = request.get_full_path()

    valid_paths = [
      reverse('needs_confirm'),
      reverse('logout'),
    ]

    in_any = any([p in path for p in valid_paths])

    if request.app_user and not request.app_user.confirmed and not in_any:
      return http.HttpResponseRedirect(reverse('needs_confirm'))