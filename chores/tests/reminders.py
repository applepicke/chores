from django.test import TestCase

from chores.models import Reminder
from chores.tasks import daily_reminders, weekly_reminders, one_off_reminders, send_reminder

class RemindersTest(TestCase):

  def test_daily_scheduled(self):


  def test_weekly_scheduled(self):
    #blah

  def test_once_scheduled(self):
    #halsdfj

  def test_run_reminder(self):