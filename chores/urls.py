from chores import views

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


  # LOGIN
  ########
  url(r'^login/$', 'chores.views.login_view', name='login'),
  url(r'^logout/$', 'chores.views.logout_view', name='logout'),
  url(r'^signup/$', 'chores.views.signup', name='signup'),

  #  FRONT FACING
  ################
  url(r'^admin/', include(admin.site.urls)),
  url(r'^needs_confirm/?$', 'chores.views.needs_confirm', name='needs_confirm'),
  url(r'^confirm_email/(?P<token>.+)/?$', 'chores.views.confirm_email', name='confirm_email'),
  url(r'^house/?$', 'chores.views.index', name='houses'),
  url(r'^house/(?P<house_id>\d+)/', 'chores.views.house', name='house'),
  url(r'^welcome/(?P<house_id>\d+)/?$', 'chores.views.welcome', name='welcome'),
  url(r'^new-house/?$', 'chores.views.new_house', name='new-house'),
  url(r'^account/?$', 'chores.views.app', name='account'),
  url(r'^invites/?$', 'chores.views.app', name='invites'),

  #  API
  ########

  #House
  url(r'^api/house/?$', 'chores.views.api_houses', name='api_houses'),
  url(r'^api/house/(?P<id>\d+)/?$', 'chores.views.api_house', name='api_house'),

  # Account
  url(r'^api/account/?$', 'chores.views.api_accounts', name='api_accounts'),
  url(r'^api/account/(?P<account_id>\d+)/?$', 'chores.views.api_account', name='api_account'),

  # Chores
  url(r'^confirm/(?P<token>.+)/$', 'chores.views.confirmation', name='confirmation'),
  url(r'^api/chore/?$', 'chores.views.api_chores', name='api_chores'),
  url(r'^api/chore/(?P<chore_id>\d+)/?$', 'chores.views.api_chore', name='api_chore'),

  # Reminders
  url(r'^api/reminder/?$', 'chores.views.api_reminder', name='api_reminders'),
  url(r'^api/reminder/(?P<reminder_id>\d+)/?$', 'chores.views.api_reminder', name='api_reminder'),

  # Invitations
  url(r'^api/invite/(?P<invite_id>\d+)/?$', 'chores.views.api_invite', name='api_invite'),

  url(r'^$', 'chores.views.index', name='index'),
  url(r'^timezones/?$', 'chores.views.timezones', name='timezones'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
