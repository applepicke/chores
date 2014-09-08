from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib import admin

from jsonfield import JSONField

class User(models.Model):
  fb_user_id = models.CharField(max_length=255, default='')
  first_name = models.CharField(max_length=255, default='')
  last_name = models.CharField(max_length=255, default='')
  email = models.CharField(max_length=255)
  phone_number = models.CharField(max_length=20, default='')
  extras = JSONField(default='{}')
  d_user = models.ForeignKey(auth_models.User, null=True)
  access_token = models.CharField(max_length=255, default='')
  confirmed = models.BooleanField(default=False)

  @property
  def name(self):
    if not self.confirmed:
      return '%s (Pending)' % self.email
    return '%s %s' % (self.first_name, self.last_name)

  @property
  def house(self):
    houses = self.owned_houses.all()
    if houses:
      return houses[0]
    return None

  @property
  def chores(self):
    return Chore.objects.filter(user__id=self.id)

  def add_d_user(self, email):
    d_user = auth_models.User.objects.filter(
      email=email,
    )

    if not d_user:
      d_user = auth_models.User.objects.create(
        email=email,
        username=email,
      )
    else:
      d_user = d_user[0]

    self.d_user = d_user

  def owns_chore(self, id):
    for house in self.owned_houses.all():
      if int(id) in [chore.id for chore in house.chores.all()]:
        return True

    return False

  def as_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'email': self.email,
      'confirmed': self.confirmed,
    }

  def __str__(self):
    return self.name

class House(models.Model):
  name = models.CharField(max_length=255)
  address = models.CharField(max_length=2000, default='', null=True)
  owner = models.ForeignKey(User, null=True, related_name="owned_houses")
  members = models.ManyToManyField(User, related_name="houses")
  recurs = models.CharField(max_length=255, default='sunday')

  @property
  def users(self):
    return [self.owner] + list(self.members.all())

  def shuffle(self):
    chores = self.chores.order_by('id')
    users = [c.user for c in chores]

    i = -1
    for chore in chores:
      chore.user = users[i]
      chore.save()
      i += 1

  def __str__(self):
    return '%s' % (
      self.name
    )

class Chore(models.Model):
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=2000, null=True, default='')
  user = models.ForeignKey(User, null=True)
  house = models.ForeignKey(House, related_name='chores')

  def __str__(self):
    return '%s' % (
      self.name
    )

  def as_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'user': self.user.as_dict() if self.user else None,
    }

class UserAdmin(admin.ModelAdmin):
    pass

class HouseAdmin(admin.ModelAdmin):
    pass

class ChoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Chore, ChoreAdmin)

