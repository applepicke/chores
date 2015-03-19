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

from chores.models import User, House, Chore, Reminder, HouseMemberRequest
from chores.utils import untokenize, rando_msg, get_timezones, tokenize
from chores.facebook_utils import Facebook, fb_get_or_create_user
from chores.context import context
from chores.users.invitations import Invitation, Confirmation

def index(request):
  user = request.app_user

  if not user or not request.user.is_authenticated():
    if not request.path_info == '/':
      return http.HttpResponseRedirect('/')
    return render_to_response('login.html', context(request))

  else:
    house = user.house
    member_of_house = user.houses.all()

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
def app(request):
  return render_to_response('app.html', context(request))

@login_required
def needs_confirm(request):
  if request.method == 'POST':
    if request.POST.get('resend'):
      confirmation = Confirmation(request.app_user, request.META['HTTP_HOST'])
      confirmation.send()

  return render_to_response('needs_confirm.html', context(request))

# Confirm signup request
@login_required
def confirm_email(request, token):
  try:
    confirmation_token = untokenize(token)
    user = request.app_user
  except:
    raise http.Http404

  if user.confirmation_token == confirmation_token:
    user.confirmed = True
    user.save()

  return http.HttpResponseRedirect('/')

# Confirm invite to household
def confirmation(request, token):
  try:
    id = untokenize(token)
    email_request = HouseMemberRequest.objects.get(id=id)
    user = email_request.user
  except:
    raise http.Http404

  if user.confirmed:
    if not user.logged_in(request):
      return http.HttpResponseRedirect('%s?next=%s' % (reverse('login'), reverse('invites')))
    else:
      return http.HttpResponseRedirect(reverse('invites'))

  else:
    return http.HttpResponseRedirect('%s?token=%s' % (reverse('signup'), token))

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
    try:
      house = user.owned_houses.get(id=request.POST.get('house_id'))
    except House.DoesNotExist:
      raise http.Http404

    email = request.REQUEST.get('email', '').strip()

    if 'email' not in request.REQUEST:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'You must enter an email address'
      }))

    existing_user = User.objects.filter(email=email)

    if existing_user:
      existing_user = existing_user[0]

    exists = existing_user in house.members.all()

    if exists:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': '%s already has a member with that email address' % house.name,
      }))

    existing_request = HouseMemberRequest.objects.filter(
      house=house,
      user__email=email,
      confirmed=True,
    )

    if existing_request and existing_user:
      house.members.add(existing_user)
      return http.HttpResponse(json.dumps({
        'member': existing_user.as_dict()
      }))

    if not existing_user:
      existing_user = house.members.create(
        email=email,
        confirmed=False,
      )

    member_request = HouseMemberRequest.objects.create(
      sender=user,
      user=existing_user,
      house=house,
      confirmed=False,
    )

    try:
      invite = Invitation(member_request, house, request.META['HTTP_HOST'])
      invite.send()
    except smtplib.SMTPException:
      return http.HttpResponse(json.dumps({
        'success': False,
        'msg': 'Could not send email to that address. You sure it\'s real?',
      }))

    return http.HttpResponse(json.dumps({
      'data': existing_user.as_dict()
    }))

  return http.HttpResponse(json.dumps({
    'data': user.account_as_dict(),
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
    'data': user.account_as_dict(),
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

  removeMember = request.POST.get('removeMember')

  if removeMember:
    member = house.members.get(id=removeMember)
    house.removeMember(member)

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
def api_invite(request, invite_id=None):
  user = request.app_user
  invite = get_object_or_404(user.invites.all(), id=invite_id)
  confirmed = request.REQUEST.get('confirmed')

  if confirmed:
    invite.confirmed = confirmed
    invite.save()

  return http.HttpResponse(json.dumps({
    'data': invite.as_dict(),
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

def signup(request):
  token = request.GET.get('token')
  email_request = None
  querystring = '?token=%s' % token if token else ''

  if token:
    try:
      id = untokenize(token)
      email_request = HouseMemberRequest.objects.get(id=id)
    except:
      raise http.Http404

  if request.method == 'POST':

    # User confirms identity with Facebook
    if 'access_token' in request.REQUEST:
      token = request.REQUEST.get('access_token')
      user_id = request.REQUEST.get('user_id')

      fb = Facebook()

      if not fb.check_user(token, user_id):
        return http.HttpResponse(json.dumps({
          'success': False,
          'msg': 'Nice try.'
        }))

      fb_get_or_create_user(fb)
      authenticated = authenticate(token=token)

    # Regular signup form
    else:
      first_name = request.REQUEST.get('first_name')
      last_name = request.REQUEST.get('last_name')
      email = request.REQUEST.get('email', '').strip()
      password = request.REQUEST.get('password')
      user = None

      ctx = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'querystring': querystring,
        'email_request': email_request,
      }

      required = [first_name, last_name, password]

      if not email_request:
        required.append(email)
      else:
        user = email_request.user

      if not all(required):
        ctx.update({
          'error': 'All fields are required',
        })
        return render_to_response('signup.html', context(request, ctx))

      if not user:
        existing_users = User.objects.filter(email=email)

        if existing_users:
          ctx.update({
            'error': rando_msg([
              'A user with that email already exists!',
              'That can\'t be your email address, someone else is using it!',
            ])
          })
          return render_to_response('signup.html', context(request, ctx))

        user = User.objects.create(
          email=email,
          confirmed=False,
        )
      else:
        user.confirmed = True

      user.first_name = first_name
      user.last_name = last_name

      if not user.d_user:
        user.add_d_user(user.email)

      user.save()
      user.d_user.set_password(password)
      user.d_user.save()

      confirmation = Confirmation(user, request.META['HTTP_HOST'])
      confirmation.send()

      authenticated = authenticate(username='%s' % user.id, password=request.REQUEST.get('password'))

    login(request, authenticated)

    if email_request:
      return http.HttpResponseRedirect(reverse('confirmation', args=(tokenize(str(email_request.id)),)))

    return http.HttpResponseRedirect('/')

  return render_to_response('signup.html', context(request, {
    'querystring': querystring,
    'next': next,
    'email_request': email_request,
  }))

def login_view(request):
  token = request.POST.get('access_token')
  user_id = request.POST.get('user_id')

  email = request.POST.get('email')
  password = request.POST.get('password')

  next = request.POST.get('next')

  def success():
    if next:
      return http.HttpResponseRedirect(next)
    else:
      return http.HttpResponse(json.dumps({
        'success': True,
        'code': 'logged-in',
      }))

  if request.POST.get('normal_auth'):
    user = User.objects.filter(email=email)

    if user:
      authenticated = authenticate(username='%s' % user[0].id, password=password)
    else:
      authenticated = None

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
    return success()

  fb = Facebook()

  if not fb.check_user(token, user_id):
    return http.HttpResponse(json.dumps({
      'success': False,
      'msg': 'Nice try.'
    }))

  fb_get_or_create_user(fb, token)

  authenticated = authenticate(token=token)
  login(request, authenticated)

  return success()

