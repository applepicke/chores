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
  url(r'^houses/', 'chores.views.index', name='houses'),

  url(r'^api/houses/?$', 'chores.views.api_houses', name='api_houses'),
  url(r'^api/houses/(?P<id>\d+)/?$', 'chores.views.api_house', name='api_house'),
  url(r'^api/houses/(?P<house_id>\d+)/chores/?$', 'chores.views.chores', name='create_chore'),
  url(r'^api/houses/(?P<house_id>\d+)/members/?$', 'chores.views.members', name='api_members'),

  url(r'^api/chores/(?P<chore_id>\d+)/?$', 'chores.views.chore', name='api_chore'),

  url(r'^$', 'chores.views.index', name='index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
