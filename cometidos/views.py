from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import *

def cometido_create(request):
	return HttpResponse("<h1>Crea Cometido<h1>")

def cometido_detail(request, id=None):
	instance = get_object_or_404(Cometido, id=id)
	context = {
		"title": "Detalle",
		"instance": instance,
	}
	return render(request, "cometido_detail.html", context)

def cometido_list(request):
	queryset = Cometido.objects.all()
	context = {
		"object_list": queryset,
		"title": "Lista Cometidos"
	}
#	if request.user.is_authenticated():
#		context = {
#			"title": "Lista de usuario"
#		}
#	else:	
#		context = {
#			"title": "Lista sin autentificacion"
#		}
	return render(request, "index.html", context)

def cometido_update(request):
	return HttpResponse("<h1>Actualizar Cometidos<h1>")

def cometido_delete(request):
	return HttpResponse("<h1>Borrar Cometidos<h1>")
