from django.conf.urls import url
from django.contrib import admin

from . views import (cometido_list,cometido_create,cometido_detail,cometido_update,cometido_delete)

urlpatterns = [
	url(r'^$', cometido_list),
	url(r'^create/$', cometido_create),
	url(r'^(?P<id>\d+)/$', cometido_detail, name='detail'),
	url(r'^update/$', cometido_update),
	url(r'^delete$', cometido_delete),
]
