from django.core import mail

from chores.models import Reminder
from chores.tests.base import ChoresTestCase
from chores.tasks import daily_reminders, weekly_reminders, one_off_reminders, send_reminder, rollover_house

class RemindersTest(ChoresTestCase):

  def test_daily_scheduled(self):
    reminder = self.daily_reminder

  def test_weekly_scheduled(self):
    reminder = self.weekly_reminder

  def test_once_scheduled(self):
    reminder = self.one_off_reminder

  def test_run_reminder(self):
    self.assertEqual(len(mail.outbox), 0)

    self.daily_reminder.send()

    self.assertEqual(len(mail.outbox), 1)

  def test_shuffle(self):
    rollover_house(self.house.id)
    self.assertEqual(len(mail.outbox), 1)