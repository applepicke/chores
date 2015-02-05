from __future__ import absolute_import

import datetime

from .celery import app
from celery.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from django.core.mail import send_mail

from chores.models import Reminder, House
from chores.utils import errorize
from chores.messages import SMS_MSG, EMAIL_MSG

@periodic_task(run_every=crontab(minute="*/1"))
def daily_reminders():
  now = datetime.datetime.utcnow()
  time_str = now.strftime('%I:%M %p')

  reminders = Reminder.objects.filter(time=time_str, type='daily').values_list('id', flat=True)
  for reminder_id in reminders:
    send_reminder.delay(reminder_id)

@periodic_task(run_every=crontab(minute="*/1"))
def weekly_reminders():
  now = datetime.datetime.utcnow()
  time_str = now.strftime('%I:%M %p')
  day_str = now.strftime('%A').lower()

  reminders = Reminder.objects.filter(time=time_str, day=day_str, type='weekly').values_list('id', flat=True)
  for reminder_id in reminders:
    send_reminder.delay(reminder_id)

@periodic_task(run_every=crontab(minute="*/1"))
def one_off_reminders():
  now = datetime.datetime.utcnow()
  now = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)

  reminders = Reminder.objects.filter(date=now, type='once').values_list('id', flat=True)
  for reminder_id in reminders:
    send_reminder.delay(reminder_id)

@periodic_task(run_every=crontab(hour=9, minute=00))
def rollover_date():
  now = datetime.datetime.utcnow()
  day = datetime.datetime.now().strftime('%A').lower()
  houses = House.objects.filter(recurs=day).values_list('id', flat=True)
  for house_id in houses:
    rollover_house.delay(house_id)

@app.task
def send_reminder(reminder_id):
  reminder = Reminder.objects.get(id=reminder_id)

  try:
    reminder.send()
  except Exception as e:
    errorize(e, 'SEND REMINDER ERROR')

@app.task
def rollover_house(house_id):
  house = House.objects.get(id=house_id)
  house.shuffle()
  for chore in house.chores.all():
    user = chore.user

    if user and user.confirmed:
      if user.email and user.email_enabled:
        send_mail(
          'Chores',
          EMAIL_MSG % (chore.name, chore.description),
          'wcurtiscollins@willyc.me',
          [user.email],
          fail_silently=False
        )

      if user.can_receive_sms:
        client = SMSClient(chore.user)
        client.send_message(SMS_MSG % (user.name, chore.name))
