from chores import views

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^login/$', 'chores.views.login', name='login'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^$', 'chores.views.index', name='index'),
)
