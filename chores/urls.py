from chores import views

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^login/$', 'chores.views.login_view', name='login'),
  url(r'^logout/$', 'chores.views.logout_view', name='logout'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^$', 'chores.views.index', name='index'),
)
