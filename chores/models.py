from django.db import models
from django.contrib.auth import models as auth_models

from jsonfield import JSONField

class User(models.Model):
  fb_user_id = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  extras = JSONField(default='{}')
  d_user = models.ForeignKey(auth_models.User)

class House(models.Model):
  name = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  owner = models.ForeignKey(User)

  def shuffle(self):
    chores = self.chores.order_by('id')

    first = None
    prev = None
    for chore in chores:
      if not first:
        first = prev = chore
        continue
      chore.user = prev.user
      chore.save()
      prev = chore

    first.user = prev.user
    first.save()

class Chore(models.Model):
  name = models.CharField(max_length=255)
  user = models.ForeignKey(User)
  active_date = models.DateField()
  house = models.ForeignKey(House, related_name='chores')

