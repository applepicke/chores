from __future__ import absolute_import

import datetime

from .celery import app
from celery.schedules import crontab
from celery.task import periodic_task

from chores.models import Reminder
from chores.utils import errorize

@periodic_task(run_every=crontab(minute="*/1"))
def daily_reminders():
  now = datetime.datetime.utcnow()
  time_str = now.strftime('%H:%M %p')

  reminders = Reminder.objects.filter(time=time_str, type='daily')
  for reminder in reminders:
    send_reminder.delay(reminder)

@periodic_task(run_every=crontab(minute="*/1"))
def weekly_reminders():
  now = datetime.datetime.utcnow()
  time_str = now.strftime('%H:%M %p')
  day_str = now.strftime('%A').lower()

  reminders = Reminder.objects.filter(time=time_str, day=day_str, type='weekly')
  for reminder in reminders:
    send_reminder.delay(reminder)

@periodic_task(run_every=crontab(minute="*/1"))
def one_off_reminders():
  now = datetime.datetime.utcnow()
  now = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)

  reminders = Reminder.objects.filter(date=now, type='once')
  for reminder in reminders:
    send_reminder.delay(reminder)

@periodic_task(run_every=crontab(minute=0, hour='*/1'))
def rollover_date():
  print('rollover')

@app.task
def send_reminder(reminder):
  try:
    reminder.send()
  except Exception as e:
    errorize(e, 'SEND REMINDER ERROR')

