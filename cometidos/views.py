from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q


# Create your views here.
from .forms import CometidoForm
from .models import *
from personas.models import *


def cometido_create(request):
	form = CometidoForm(request.POST or None)
	if form.is_valid():
		persona = Persona.objects.get(pk=request.user)
		instance = form.save(commit=False)
		instance.rut = persona.rut
		instance.nombre = request.user.first_name + ' ' + request.user.last_name
		instance.grado = persona.grado
		instance.escalafon = persona.escalafon
		instance.estamento = persona.estamento
		instance.unidad = persona.unidad
		instance.region = persona.region
                instance.persona = request.user
                instance.save()
                messages.success(request, 'Creado satisfactoriamente')
                return HttpResponseRedirect(instance.get_absolute_url())
	else:
		persona = Persona.objects.get(pk=request.user)
		data = {
			'rut': persona.rut,
			'nombre': request.user.first_name + ' ' + request.user.last_name,
			'grado': persona.grado,
			'escalafon': persona.escalafon,
			'estamento': persona.estamento,
			'unidad': persona.unidad,
			'region': persona.region
		}
		form = CometidoForm(initial=data)

	context = {
		"form": form,
	}
	return render(request, "cometido_form.html", context)

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
