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
      'id': house.id,
      'name': house.name,
      'users': [user.as_dict() for user in house.users],
      'owner': house.owner.as_dict(),
      'chores': [chore.as_dict() for chore in house.chores.all()],
    },
  }))

@login_required
def chores(request, house_id):
  user = request.app_user

  try:
    house = user.owned_houses.get(id=house_id)
  except House.DoesNotExist:
    raise Http404

  if request.method == "POST":

    user = [user for user in house.users if str(user.id) == request.REQUEST.get('userId', '')]

    if not user:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'User does not exist in this household',
      }))

    if len(user) > 1:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'Uh oh. There is more than one user with that id. We fudged up, but we\'ll fix it for you!',
      }))

    user = user[0]

    try:
      db_chore = house.chores.get(id=request.REQUEST.get('id'))
      db_chore.name = request.REQUEST.get('name')
      db_chore.description = request.REQUEST.get('description')
      db_chore.user = user
      db_chore.save()
      created = False
    except Chore.DoesNotExist:
      db_chore = house.chores.create(
        name=request.REQUEST.get('name'),
        description=request.REQUEST.get('description'),
        user=user,
      )
      created = True

    return http.HttpResponse(json.dumps({
      'created': created,
      'success': True,
      'chore': {
        'name': db_chore.name,
        'description': db_chore.description,
        'user': user.as_dict(),
      },
    }))

  chores = house.chores.all()
  return http.HttpResponse(json.dumps({
    'chores': [chore.as_dict() for chore in chores]
  }))

@login_required
def chore(request, chore_id):
  user = request.app_user

  try:
    chore = Chore.objects.get(id=chore_id)
  except Chore.DoesNotExist:
    raise http.Http404

  if not user.owns_chore(chore_id):
    raise http.Http404

  if request.method == 'DELETE':
    chore.delete()
    return http.HttpResponse(json.dumps({
      'success': True,
      'id': int(chore_id),
    }))

  raise http.Http404

@login_required
def user_request(request, house_id):
  user = app_user

  try:
    house = user.owned_houses.get(id=house_id)
  except House.DoesNotExist:
    raise http.Http404

  if 'email' not in request.REQUEST:
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'You must enter an email address'
    }))

  house.members.create(
    email=request.REQUEST.get('email'),
    confirmed=False
  )

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
      email=obj.get('email'),
      username=user.fb_user_id,
    )
    user.email = obj.get('email')
    user.first_name = obj.get('first_name')
    user.last_name = obj.get('last_name')
    user.d_user.set_password(settings.GENERIC_USER_PASSWORD)
    user.d_user.save()
    user.confirmed = True
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

