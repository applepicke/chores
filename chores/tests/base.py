import datetime

from model_mommy import mommy

from django.test import TestCase

class ChoresTestCase(TestCase):

  def setUp(self):
    self.user = mommy.make('chores.User', email='test@test.com')
    self.user2 = mommy.make('chores.User', email='test@test2.com')
    self.user3 = mommy.make('chores.User', email='test@test3.com')

    self.house = mommy.make('chores.House', owner=self.user)

    self.user.email_enabled = True
    self.user.sms_enabled = False
    self.user.save()

    self.chore1 = mommy.make('chores.Chore', house=self.house, users=[self.user])
    self.chore2 = mommy.make('chores.Chore', house=self.house, users=[self.user])
    self.chore3 = mommy.make('chores.Chore', house=self.house, users=[self.user])

    self.setUpReminders()

  def setUpReminders(self):
    self.now = datetime.datetime.utcnow()
    time = self.now.strftime('%I:%M %p')

    self.daily_reminder = mommy.make('chores.Reminder',
      type='daily',
      time=time,
      chore=self.chore1,
    )
    self.weekly_reminder = mommy.make('chores.Reminder',
      type='weekly',
      day=self.now.strftime('%A').lower(),
      time=time,
      chore=self.chore2,
    )
    self.one_off_reminder = mommy.make('chores.Reminder',
      type='once',
      date=self.now,
      time=time,
      chore=self.chore3,
    )

