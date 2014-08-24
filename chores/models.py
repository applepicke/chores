from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib import admin

from jsonfield import JSONField

class User(models.Model):
  fb_user_id = models.CharField(max_length=255)
  first_name = models.CharField(max_length=255, default='')
  last_name = models.CharField(max_length=255, default='')
  email = models.CharField(max_length=255)
  extras = JSONField(default='{}')
  d_user = models.ForeignKey(auth_models.User, null=True)
  access_token = models.CharField(max_length=255)

  def __str__(self):
    return '%s %s - %s' % (
      self.first_name,
      self.last_name,
      self.email
    )

class House(models.Model):
  name = models.CharField(max_length=255)
  address = models.CharField(max_length=2000)
  owner = models.ForeignKey(User, null=True)
  recurs = models.CharField(max_length=255)

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

    def __str__(self):
      return '%s' % (
        self.name
      )

class Chore(models.Model):
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=2000)
  user = models.ForeignKey(User, null=True)
  house = models.ForeignKey(House, related_name='chores')

  def __str__(self):
    return '%s' % (
      self.name
    )

class UserAdmin(admin.ModelAdmin):
    pass

class HouseAdmin(admin.ModelAdmin):
    pass

class ChoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Chore, ChoreAdmin)

