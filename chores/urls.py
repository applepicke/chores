from chores import views

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^login/$', 'chores.views.login_view', name='login'),
  url(r'^logout/$', 'chores.views.logout_view', name='logout'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^house/?$', 'chores.views.index', name='houses'),
  url(r'^house/(?P<house_id>\d+)/', 'chores.views.house', name='house'),
  url(r'^welcome/?$', 'chores.views.welcome', name='welcome'),
  url(r'^account/?$', 'chores.views.account', name='account'),

  url(r'^api/house/?$', 'chores.views.api_houses', name='api_houses'),
  # url(r'^api/house/my_house?$', 'chores.views.api_my_house', name='api_my_house'),
  url(r'^api/house/(?P<id>\d+)/?$', 'chores.views.api_house', name='api_house'),
  url(r'^api/house/(?P<house_id>\d+)/members/?$', 'chores.views.members', name='api_members'),

  url(r'^api/account/?$', 'chores.views.api_accounts', name='api_accounts'),
  url(r'^api/account/(?P<account_id>\d+)/?$', 'chores.views.api_account', name='api_account'),

  url(r'^confirm/(?P<token>.+)/$', 'chores.views.confirmation', name='confirmation'),
  url(r'^api/chore/?$', 'chores.views.api_chores', name='api_chores'),
  url(r'^api/chore/(?P<chore_id>\d+)/?$', 'chores.views.api_chore', name='api_chore'),

  url(r'^api/reminder/?$', 'chores.views.api_reminder', name='api_reminders'),
  url(r'^api/reminder/(?P<reminder_id>\d+)/?$', 'chores.views.api_reminder', name='api_reminder'),

  url(r'^$', 'chores.views.index', name='index'),
  url(r'^timezones/?$', 'chores.views.timezones', name='timezones'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
