import json
import facebook

from django import http
from django.conf import settings
from django.contrib.auth import models as auth_models, login
from django.shortcuts import render_to_response

from chores.models import User
from chores.utils import Facebook
from chores.context import context

def index(request):

  if not request.user.is_authenticated():
    return render_to_response('login.html', context(request))

  return render_to_response('app.html', context(request))

def login(request):

  token = request.POST.get('access_token')
  user_id = request.POST.get('user_id')

  fb = Facebook()

  if not fb.check_user(token, user_id):
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'Nice try.'
    }))

  try:
    user, created = User.objects.get_or_create(
      fb_user_id=fb.user_info.get('user_id'),
    )
  except User.MultipleObjectsReturned:
    user = User.objects.filter(
      fb_user_id=fb.user_info.get('user_id')
    ).latest('id')
    created = False

  graph = facebook.GraphAPI(token)
  obj = graph.get_object('me')

  if created or not user.d_user:
    user.d_user, created = auth_models.User.objects.get_or_create(
      email='%s@chores.dev' % user.fb_user_id,
      username=user.fb_user_id,
    )
    user.email = obj.get('email')
    user.first_name = obj.get('first_name')
    user.last_name = obj.get('last_name')
    user.d_user.set_password(settings.GENERIC_USER_PASSWORD)
    user.d_user.save()
    user.save()

  user.access_token = token
  user.save()

  if not user.d_user.is_authenticated():
    login(request, user.d_user)

  return http.HttpResponse(json.dumps({
    'success': True,
    'code': 'logged-in',
    'created': created,
  }))

