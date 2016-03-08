from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
	url(r'^$', "cometidos.views.cometido_list"),
	url(r'^create/$', "cometidos.views.cometido_create"),
	url(r'^detail/$', "cometidos.views.cometido_detail"),
	url(r'^update/$', "cometidos.views.cometido_update"),
	url(r'^delete$', "cometidos.views.cometido_delete"),
]
