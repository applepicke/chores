import datetime

from model_mommy import mommy

from django.test import TestCase

class ChoresTestCase(TestCase):

  def setUp(self):
    self.user = mommy.make('chores.User', email='test@test.com')
    self.house = mommy.make('chores.House', owner=self.user)

    self.setUpReminders()

  def setUpReminders(self):
    self.now = datetime.datetime.utcnow()
    time = self.now.strftime('%H:%M %p')

    self.daily_reminder = mommy.make('chores.Reminder',
      type='daily',
      time=time,
    )
    self.weekly_reminder = mommy.make('chores.Reminder',
      type='weekly',
      day=self.now.strftime('%A').lower(),
      time=time,
    )
    self.one_off_reminder = mommy.make('chores.Reminder',
      type='once',
      date=self.now,
      time=time,
    )

