from __future__ import absolute_import
from .celery import app
from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(minute="*/1"))
def daily_reminders():
  print('fetching daily')

@periodic_task(run_every=crontab(minute="*/1"))
def weekly_reminders():
  print('fetching weekly')

@periodic_task(run_every=crontab(minute="*/1"))
def one_off_reminders():
  print('fetching one off')

@periodic_task(run_every=crontab(minute=0, hour='*/1'))
def rollover_date():
  print('rollover')

