from django.conf.urls import url
from django.contrib import admin

from .views import (cometido_list,cometido_create,cometido_detail,cometido_update,cometido_delete,cometido_print)

urlpatterns = [
	url(r'^$', cometido_list),
	url(r'^crear/$', cometido_create),
	url(r'^(?P<id>\d+)/$', cometido_detail, name='detail'),
	url(r'^(?P<id>\d+)/edit/$', cometido_update, name='update'),
	url(r'^delete$', cometido_delete),
	url(r'^(?P<id>\d+)/print$', cometido_print),
]
