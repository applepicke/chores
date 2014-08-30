import facebook

from chores.models import User

class FacebookBackend(object):
  def authenticate(self, token=None):
    try:
      graph = facebook.GraphAPI(token)
    except facebook.GraphAPIError:
      return None

    obj = graph.get_object('me')

    user = User.objects.get(fb_user_id=obj.get('id'))

    if not user.d_user:
      return None

    return user.d_user

  def get_user(self, user_id):
    try:
      return User.objects.filter(d_user__pk=user_id).latest('id').d_user
    except User.DoesNotExist:
      return None
