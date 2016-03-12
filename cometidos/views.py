from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CometidoForm
from .models import *
from personas.models import *

@login_required
def cometido_create(request):
	form = CometidoForm(request.POST or None)
	if form.is_valid():
		persona = Persona.objects.get(pk=request.user)
		instance = form.save(commit=False)
		instance.rut = persona.rut
                instance.persona = request.user
                instance.save()
                messages.success(request, 'Cometido creado satisfactoriamente')
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

@login_required
def cometido_detail(request, id=None):
	instance = get_object_or_404(Cometido, id=id)
	context = {
		"title": "Detalle",
		"instance": instance,
	}
	return render(request, "cometido_detail.html", context)

@login_required
def cometido_list(request):
	queryset = Cometido.objects.all()
	context = {
		"object_list": queryset,
		"title": "Lista Cometidos"
	}
	return render(request, "cometidos/index.html", context)

@login_required
def cometido_update(request, id=None):
	instance = get_object_or_404(Cometido, id=id)
	form = CometidoForm(request.POST or None, instance=instance)
        if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Cometido actualizado satisfactoriamente')
                return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"instance": instance,
		"form": form,
	}
	return render(request, "cometido_form.html", context)


def cometido_delete(request):
	return HttpResponse("<h1>Borrar Cometidos<h1>")
