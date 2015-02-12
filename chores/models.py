import datetime
import pytz

from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings

from jsonfield import JSONField

from chores.cache import CachedSMSVerificationCode
from chores.utils import random_string, to_utc, from_utc, gravatar, user_time
from chores.sms import SMSClient
from chores.messages import DEFAULT_REMINDER_SMS_MSG, DEFAULT_REMINDER_EMAIL_MSG

class User(models.Model):
  fb_user_id = models.CharField(max_length=255, default='')
  first_name = models.CharField(max_length=255, default='')
  last_name = models.CharField(max_length=255, default='')
  email = models.CharField(max_length=255)
  phone_number = models.CharField(max_length=20, default='')
  extras = JSONField(default='{}')
  d_user = models.ForeignKey(auth_models.User, null=True)
  access_token = models.CharField(max_length=255, default='')
  confirmed = models.BooleanField(default=False)
  email_enabled = models.BooleanField(default=True)
  sms_enabled = models.BooleanField(default=False)
  sms_verified = models.BooleanField(default=False)
  sms_banned = models.BooleanField(default=False)
  timezone = models.CharField(max_length=1024, default='UTC')

  @property
  def full_name(self):
    return '%s %s' % (self.first_name, self.last_name)

  @property
  def avatar(self):
    return gravatar(self.email)

  @property
  def has_password(self):
    if self.d_user:
      return self.d_user.has_usable_password()
    return False

  @property
  def name(self):
    if not self.confirmed:
      return '%s (Pending)' % self.email
    return '%s %s' % (self.first_name, self.last_name)

  @property
  def house(self):
    houses = self.owned_houses.all()
    if houses:
      return houses[0]
    return None

  @property
  def chores(self):
    return Chore.objects.filter(user__id=self.id)

  @property
  def editable_chores(self):
    return Chore.objects.filter(house__owner__id=self.id)

  @property
  def can_receive_sms(self):
    return self.sms_enabled and self.sms_verified and self.phone_number and not self.sms_banned

  def send_message(self, email_message='', sms_message=''):
    if self.confirmed:
      if self.email and self.email_enabled and email_message:
        send_mail(
          'Chores',
          email_message,
          'wcurtiscollins@willyc.me',
          [self.email],
          fail_silently=False
        )

      if self.can_receive_sms and sms_message:
        client = SMSClient(self)
        client.send_message(sms_message)

  def change_phone_number(self, number):
    number = number.replace('-', '')
    number = number.replace(' ', '')
    if not number.startswith('+'):
      number = '+%s' % number
    self.phone_number = number
    self.save()

  def send_sms_verification_code(self, number):
    code = random_string()
    cached_code = CachedSMSVerificationCode(user_id=self.id)
    cached_code.set(code)

    self.change_phone_number(number)
    self.save()

    client = SMSClient(self)
    client.send_verification_code(code, number)

  def verify_sms(self, code):
    cached_code = CachedSMSVerificationCode(user_id=self.id).get()

    if not cached_code:
      return False, 'Your verification code has expired.'

    if cached_code == code:
      self.sms_verified = True
      self.sms_enabled = True
      self.save()
      return True, ''

    return False, 'Invalid verification code.'

  def can_edit_house(self, house):
    return house.owner == self

  def add_d_user(self, email):
    d_user = auth_models.User.objects.filter(
      username=email,
    )

    if not d_user:
      d_user = auth_models.User.objects.create(
        email=email,
        username=email,
      )
    else:
      d_user = d_user[0]

    self.d_user = d_user
    self.save()

  def can_modify_chore(self, chore):
    if self.owns_chore(chore.id):
      return True

  def owns_chore(self, id):
    for house in self.owned_houses.all():
      if int(id) in [chore.id for chore in house.chores.all()]:
        return True

    return False

  def get_timezone(self):
    if not self.timezone:
      return pytz.UTC
    return pytz.timezone(self.timezone)

  def short_timezone(self):
    return from_utc(datetime.datetime.now(), self).strftime('%Z')

  def as_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'email': self.email,
      'confirmed': self.confirmed,
      'has_password': self.has_password,
      'email_enabled': self.email_enabled,
      'sms_enabled': self.sms_enabled,
      'sms_verified': self.sms_verified,
      'phone_number': self.phone_number,
      'timezone': self.timezone or 'UTC',
    }

  def __str__(self):
    return self.name

class House(models.Model):
  name = models.CharField(max_length=255)
  address = models.CharField(max_length=2000, default='', null=True)
  owner = models.ForeignKey(User, null=True, related_name="owned_houses")
  members = models.ManyToManyField(User, related_name="houses")

  recurs = models.CharField(max_length=255, default='sunday')
  recurs_hour = models.CharField(max_length=255, default='0:00')

  @property
  def users(self):
    return [self.owner] + list(self.members.all())

  def shuffle(self):
    chores = self.chores.order_by('id')
    users = [c.user for c in chores]

    i = -1
    for chore in chores:
      chore.users = [users[i]] if users[i] else []
      chore.save()
      i += 1

  def __str__(self):
    return '%s' % (
      self.name
    )

  def as_dict(self, user=None):
    return {
      'id': self.id,
      'name': self.name,
      'members': [m.as_dict() for m in self.users if m],
      'chores': [c.as_dict(user=user) for c in self.chores.all()],
      'recurs': self.recurs,
    }

class Chore(models.Model):
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=2000, null=True, default='')
  users = models.ManyToManyField(User, null=True, related_name='chores')
  house = models.ForeignKey(House, related_name='chores')

  def __str__(self):
    return '%s' % (
      self.name
    )

  @property
  def user(self):
    users = self.users.all()
    return users[0] if users else None

  def parse_assigned(self, raw_assigned):
    users = []
    for u in raw_assigned or []:
      try:
        u = next(_u for _u in self.house.users if _u.id == u)
      except:
        continue
      users.append(u)
    return users

  def as_dict(self, user=None):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'assigned': self.users.all()[0].as_dict() if self.users.all().exists() else None,
      'house_id': self.house.id,
      'reminder': [r.as_dict(user=user) for r in self.reminders.all()][0] if self.reminders.count() else None,
    }

class Reminder(models.Model):
  type = models.CharField(max_length=255)
  date = models.DateTimeField(default=datetime.datetime.utcnow())
  day = models.CharField(max_length=255, default='')
  time = models.CharField(max_length=255, default='')
  chore = models.ForeignKey(Chore, related_name="reminders", null=True)
  needs_run = models.BooleanField(default=False)

  def format_for_save(self, user):
    now = datetime.datetime.now()
    self.day = self.day or ''
    self.time = self.time or ''

    if type == 'once':
      date = datetime.datetime.strptime('%s %s' % (self.date, self.time), '%m/%d/%Y %I:%M %p')
      self.date = to_utc(date, user)
    else:
      self.date = datetime.datetime.utcnow()

    time = datetime.datetime.strptime(self.time, '%I:%M %p')
    time = time.replace(year=now.year, month = now.month, day=now.day)
    self.time = to_utc(time, user).strftime('%I:%M %p')

  def get_time(self, user):
    return user_time(self.time, user)

  def send(self):
    if not self.chore:
      raise Exception('Reminder has no chore')

    chore = self.chore
    users = chore.users.all()

    if not users:
      raise Exception('Chore has no user')

    for user in users:
      user.send_message(
        email_message=DEFAULT_REMINDER_EMAIL_MSG % (chore.name, chore.description),
        sms_message=DEFAULT_REMINDER_SMS_MSG % chore.name,
      )

  def as_dict(self, user=None):
    return {
      'id': self.id,
      'type': self.type,
      'date': self.date.strftime('%m/%d/%Y'),
      'day': self.day,
      'time': self.get_time(user) if user else self.time,
      'chore_id': self.chore.id,
    }

class UserAdmin(admin.ModelAdmin):
  pass

class HouseAdmin(admin.ModelAdmin):
  pass

class ChoreAdmin(admin.ModelAdmin):
  pass

class ReminderAdmin(admin.ModelAdmin):
  pass

admin.site.register(User, UserAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Chore, ChoreAdmin)

