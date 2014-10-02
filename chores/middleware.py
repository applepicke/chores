import json

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