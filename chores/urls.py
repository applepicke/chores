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
  url(r'^houses/$', 'chores.views.index', name='houses'),
  url(r'^house/(?P<id>\d+)/$', 'chores.views.index', name='house'),

  url(r'^api/houses/$', 'chores.views.get_houses', name='get_houses'),
  url(r'^api/house/(?P<id>\d+)/$', 'chores.views.get_house_detail', name='get_house_detail'),

  url(r'^$', 'chores.views.index', name='index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
