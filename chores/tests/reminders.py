from chores.models import Reminder
from chores.tests.base import ChoresTestCase
from chores.tasks import daily_reminders, weekly_reminders, one_off_reminders, send_reminder

class RemindersTest(ChoresTestCase):

  def test_daily_scheduled(self):
    reminder = self.daily_reminder

  def test_weekly_scheduled(self):
    reminder = self.weekly_reminder

  def test_once_scheduled(self):
    reminder = self.one_off_reminder

  def test_run_reminder(self):
    pass