import json
import facebook
import smtplib
import datetime
import operator

from django import http
from django.conf import settings
from django.contrib.auth import models as auth_models, login, logout, authenticate
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from chores.models import User, House, Chore, Reminder
from chores.utils import Facebook, untokenize, rando_msg, get_timezones
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
  user = request.app_user

  try:
    house = House.objects.get(id=house_id)
  except House.DoesNotExist:
    return http.HttpResponseRedirect('/')

  if not user.can_edit_house(house):
    return http.HttpResponseRedirect('/')

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
def api_accounts(request):
  user = request.app_user

  if not user:
    raise http.Http404

  if request.method == 'POST':
    # ADD MEMBER
    if request.POST.get('email') and request.POST.get('house_id'):

      try:
        house = user.owned_houses.get(id=request.POST.get('house_id'))
      except House.DoesNotExist:
        raise http.Http404

      existing_user = User.objects.filter(email=request.REQUEST.get('email'))

      if existing_user:
        existing_user = existing_user[0]

      exists = existing_user in house.members.all()

      if exists:
        return http.HttpResponse(json.dumps({
          'msg': '%s already has a member with that email address' % house.name,
        }), 400)

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
        if not existing_user:
          member.delete()

        return http.HttpResponse(json.dumps({
          'msg': 'Could not send email to that address. You sure it\'s real?',
        }), 400)

      return http.HttpResponse(json.dumps({
        'data': member.as_dict()
      }))

  return http.HttpResponse(json.dumps({
    'data': user.as_dict(),
  }))

@login_required
def api_account(request, account_id):
  user = request.app_user

  if not user:
    raise http.Http404

  if request.method == 'PUT':
    password = request.POST.get('password')

    # SET PASSWORD
    if password:
      try:
        user.d_user.set_password(password)
        user.d_user.save()
      except:
        return http.HttpResponse(json.dumps({
          'msg': 'Hmmm, can\'t set password. Not quite sure why. Sorry.',
          'type': 'password',
        }), status=400)

    # SEND SMS VERIFICATION
    elif request.POST.get('send_sms_verification_code'):
      if user.sms_banned:
        return http.HttpResponse(json.dumps({
          'msg': 'Your account has been banned from using sms services.',
          'type': 'sms_send_verify',
        }), status=400)

      user.send_sms_verification_code(request.POST.get('sms'))

    # VERIFY SMS
    elif request.POST.get('verify_sms'):
      code = request.POST.get('sms_code')
      verified, msg = user.verify_sms(code)

      if not verified:
        return http.HttpResponse(json.dumps({
          'msg': msg,
          'type': 'sms_verify',
        }), status=400)

    # ACCOUNT INFO SAVE
    else:
      user.first_name = request.POST.get('first_name')
      user.last_name = request.POST.get('last_name')
      user.email_enabled = request.POST.get('email_enabled')
      user.sms_enabled = request.POST.get('sms_enabled')
      user.timezone = request.POST.get('timezone')
      user.save()

  return http.HttpResponse(json.dumps({
    'data': user.as_dict(),
  }))

@login_required
def api_houses(request):
  user = request.app_user
  houses = list(user.houses.all()) + list(user.owned_houses.all())

  if request.method == 'POST':

    name = request.POST.get('name', '')

    if name:
      house = House.objects.create(name=name, owner=user)

      if not house:
        return http.HttpResponse(json.dumps({
          'msg': 'Something went terribly wrong!',
        }), status=400)

      return http.HttpResponse(json.dumps({
        'data': house.as_dict(user=user),
      }))

  house_id = request.GET.get('id')

  if house_id:
    houses = [house for house in houses if str(house.id) == house_id]

  return http.HttpResponse(json.dumps({
    'count': len(houses),
    'data': [house.as_dict(user=user) for house in houses]
  }))

@login_required
def api_house(request, id):
  user = request.app_user

  try:
    house = user.owned_houses.get(id=id)
  except House.DoesNotExist:
    raise http.Http404

  name = request.POST.get('name', '')

  if name:
    house.name = name
    house.save()

    return http.HttpResponse(json.dumps({
      'data': house.as_dict(user=user),
    }))

  recurs = request.POST.get('recurs')

  if recurs:
    house.recurs = recurs
    house.save()

    return http.HttpResponse()

  return http.HttpResponse(json.dumps({
    'data': house.as_dict(user=user),
  }))

@login_required
def api_reminder(request, reminder_id=None):
  user = request.app_user

  chore_id = request.REQUEST.get('chore_id')
  chore = get_object_or_404(user.editable_chores, id=chore_id)

  if reminder_id:
    reminder = chore.reminders.get(id=reminder_id)
  else:
    reminder = Reminder()

  reminder.type = request.REQUEST.get('type')
  reminder.date = request.REQUEST.get('date', '')
  reminder.day = request.REQUEST.get('day', '')
  reminder.time = request.REQUEST.get('time', '')

  reminder.format_for_save(user)

  reminder.save()
  chore.reminders = [reminder]

  return http.HttpResponse(json.dumps({
    'data': reminder.as_dict(user=user),
  }))

@login_required
def api_chores(request, house_id=None):
  user = request.app_user

  if not house_id:
    house_id = request.POST.get('house_id')

  if not house_id:
    raise http.Http404

  try:
    house = user.owned_houses.get(id=house_id)
  except House.DoesNotExist:
    raise Http404

  if request.method == "POST":
    db_chore = house.chores.create(
      name=request.REQUEST.get('name'),
      description=request.REQUEST.get('description'),
    )

    db_chore.users = db_chore.parse_assigned(request.POST.get('assigned'))

    return http.HttpResponse(json.dumps({
      'data': db_chore.as_dict(user=user)
    }))

  chores = house.chores.all()
  return http.HttpResponse(json.dumps({
    'chores': [chore.as_dict(user=user) for chore in chores]
  }))

@login_required
def api_chore(request, chore_id):
  user = request.app_user

  db_chore = get_object_or_404(Chore.objects.all(), id=chore_id)

  house = user.owned_houses.filter(id=request.POST.get('house_id'))[:1]
  house = house.get() if house else None

  if house and db_chore in house.chores.all() and not user.can_modify_chore(db_chore):
    raise http.Http404

  if request.method == "PUT":
    db_chore.users = db_chore.parse_assigned(request.POST.get('assigned'))
    db_chore.name = request.REQUEST.get('name')
    db_chore.description = request.REQUEST.get('description')
    db_chore.save()

    return http.HttpResponse(json.dumps({
      'data': db_chore.as_dict(user=user)
    }))

  if request.method == 'DELETE':
    db_chore.delete()
    return http.HttpResponse(json.dumps({
      'id': int(chore_id),
    }))

  raise http.Http404

@login_required
def timezones(request):
  timezones = get_timezones().values()
  timezones = sorted(timezones, key=operator.itemgetter('key'))
  return http.HttpResponse(json.dumps(timezones))

@login_required
def members(request, house_id):
  user = request.app_user

  house = get_object_or_404(user.owned_houses.all(), id=house_id)

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

