from chores.models import User

class UserMiddleware(object):
  def process_request(self, request):

    try:
      request.app_user = User.objects.filter(d_user__id=request.user.id).latest('id')
    except:
      request.app_user = None

    return None