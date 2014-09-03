import json
import facebook

from django import http
from django.conf import settings
from django.contrib.auth import models as auth_models, login, logout, authenticate
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from chores.models import User, House, Chore
from chores.utils import Facebook
from chores.context import context

def index(request):

  if not request.user.is_authenticated():
    return render_to_response('login.html', context(request))

  return render_to_response('app.html', context(request))

def logout_view(request):
  logout(request)
  return http.HttpResponseRedirect('/')

@login_required
def api_houses(request):
  user = request.app_user
  houses = user.houses

  if request.method == 'POST':
    name = request.REQUEST.get('name', '')

    if not name:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'Did you forget to enter a name for your household?',
      }))

    #house = House.objects.create(name=name, owner=user)
    house = {
      'id': 1
    }

    if not house:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'Something went terribly wrong!',
      }))

    return http.HttpResponse(json.dumps({
      'success': True,
      'id': house.get('id'),
    }))

  return http.HttpResponse(json.dumps({
    'count': len(houses),
    'houses': [{
      'name': house.name
    } for house in houses]
  }))

@login_required
def api_house(request, id):
  user = request.app_user

  try:
    house = user.owned_houses.get(id=id)
  except House.DoesNotExist:
    raise http.Http404

  return http.HttpResponse(json.dumps({
    'success': True,
    'house': {
      'name': house.name,
      'users': [user.as_dict() for user in house.users],
      'chores': [chore.as_dict() for chore in house.chores.all()],
    },
  }))

@login_required
def create_chore(request, house_id):
  user = request.app_user

  try:
    house = user.owned_houses.get(id=id)
  except House.DoesNotExist:
    raise Http404

  chore = json.loads(request.POST.get('chore', '[]'))
  user = [user for user in house.users if user.email == chore.get('user', '')]

  if not user:
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'Household does not contain a user with that email address',
    }))

  if len(user) > 1:
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'Uh oh. There is more than one user with that email. We fudged up, but we\'ll fix it for you!',
    }))

  user = user[0]

  db_chore = house.chores.create(
    name=chore.get('name'),
    description=chore.get('description'),
    user=user,
  )

  return http.HttpResponse(json.dumps({
    'success': True,
    'chore': {
      'name': db_chore.name,
      'description': db_chore.description,
      'user': user.as_dict(),
    },
  }))


def login_view(request):

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

  try:
    graph = facebook.GraphAPI(token)
  except facebook.GraphAPIError:
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'Quit trying to sneak in.'
    }))

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

  authenticated = authenticate(token=token)
  login(request, authenticated)

  return http.HttpResponse(json.dumps({
    'success': True,
    'code': 'logged-in',
    'created': created,
  }))

