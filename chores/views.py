import json
import facebook
import smtplib

from django import http
from django.conf import settings
from django.contrib.auth import models as auth_models, login, logout, authenticate
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from chores.models import User, House, Chore
from chores.utils import Facebook, untokenize, rando_msg
from chores.context import context
from chores.users.invitations import Invitation

def index(request):

  if not request.user.is_authenticated():
    if not request.path_info == '/':
      return http.HttpResponseRedirect('/')
    return render_to_response('login.html', context(request))

  else:
    house = request.app_user.house
    member_of_house = request.app_user.houses.all()

    if house:
      return http.HttpResponseRedirect(reverse('house', args=(house.id,)))
    elif member_of_house:
      return http.HttpResponseRedirect(reverse('account'))
    else:
      return http.HttpResponseRedirect(reverse('welcome'))

  return render_to_response('app.html', context(request))

@login_required
def house(request, house_id):
  return render_to_response('app.html', context(request))

@login_required
def account(request):
  return render_to_response('app.html', context(request))

@login_required
def welcome(request):
  return render_to_response('app.html', context(request))

@login_required
def logout_view(request):
  logout(request)
  return http.HttpResponseRedirect('/')

@login_required
def api_account(request):
  user = request.app_user

  if not user:
    raise http.Http404

  if request.method == 'POST':
    password = request.JSON.get('password')
    confirm = request.JSON.get('confirm_password')

    if not password or password.strip() != confirm.strip():
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'Passwords don\'t match',
      }))

    try:
      user.d_user.set_password(password)
      user.d_user.save()
    except:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'Hmmm, can\'t set password. Not quite sure why. Sorry.',
      }))

    return http.HttpResponse(json.dumps({
      'success': True,
      'account': user.as_dict(),
    }))

  return http.HttpResponse(json.dumps(user.as_dict()))

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

    house = House.objects.create(name=name, owner=user)

    if not house:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'Something went terribly wrong!',
      }))

    return http.HttpResponse(json.dumps({
      'success': True,
      'id': house.id,
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
      'members': [user.as_dict() for user in house.users],
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
def members(request, house_id):
  user = request.app_user

  try:
    house = user.owned_houses.get(id=house_id)
  except House.DoesNotExist:
    raise http.Http404

  if 'email' not in request.REQUEST:
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'You must enter an email address'
    }))

  existing_user = User.objects.filter(email=request.REQUEST.get('email'))

  if existing_user:
    existing_user = existing_user[0]

  exists = existing_user in house.members.all()

  if exists:
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': '%s already has a member with that email address' % house.name,
    }))

  if not existing_user:
    member = house.members.create(
      email=request.REQUEST.get('email'),
      confirmed=False,
    )
  else:
    member = existing_user
    member.houses.add(house)
    member.save()

  try:
    invite = Invitation(member, house, request.META['HTTP_HOST'])
    invite.send()
  except smtplib.SMTPException:
    if member.id != existing_user.id:
      member.delete()

    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'Could not send email to that address. You sure it\'s real?',
    }))

  return http.HttpResponse(json.dumps({
    'success': True,
    'member': member.as_dict()
  }))

def confirmation(request, token):
  try:
    id = untokenize(token)
    user = User.objects.get(id=id)
  except:
    raise http.Http404

  if user.d_user and user.d_user.is_authenticated() and user.d_user == request.user:
    return http.HttpResponseRedirect('/')

  if request.method == 'POST':

    # User confirms identity with Facebook
    if 'access_token' in request.REQUEST:
      token = request.REQUEST.get('access_token')
      user_id = request.REQUEST.get('user_id')
      fb = Facebook()

      try:
        graph = facebook.GraphAPI(token)
      except facebook.GraphAPIError:
        return http.HttpResponse(json.dumps({
          'success': False,
          'msg': 'Quit trying to sneak in.'
        }))

      obj = graph.get_object('me')
      user.add_d_user(user.email)
      user.first_name = obj.get('first_name')
      user.last_name = obj.get('last_name')
      user.fb_user_id = obj.get('id')
      user.confirmed = True
      user.save()
      authenticated = authenticate(token=token)

    # Regular signup form
    else:
      user.first_name = request.REQUEST.get('first_name')
      user.last_name = request.REQUEST.get('last_name')

      if not request.REQUEST.get('password') == request.REQUEST.get('confirm_password'):
        return http.HttpResponse(json.dumps({
          'success': False,
          'msg': 'Passwords need to match',
        }))

      user.add_d_user(user.email)
      user.confirmed = True
      user.d_user.set_password(request.REQUEST.get('password'))
      user.save()
      authenticated = authenticate(username=user.email, password=request.REQUEST.get('password'))

    login(request, authenticated)
    return http.HttpResponseRedirect('/')

  return render_to_response('confirmation.html', context(request))

def login_view(request):
  token = request.POST.get('access_token')
  user_id = request.POST.get('user_id')

  email = request.POST.get('email')
  password = request.POST.get('password')

  if request.POST.get('normal_auth'):
    authenticated = authenticate(username=email, password=password)

    if not authenticated:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': rando_msg([
          'Nope. That\'s not right!',
          'Comon, now you\'re just guessing',
          'You\'ll get it someday',
        ]),
      }))

    login(request, authenticated)
    return http.HttpResponse(json.dumps({
      'success': True,
    }))

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
    user.add_d_user(obj.get('email'))
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

