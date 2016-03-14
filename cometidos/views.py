from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig, SingleTableView
from .tables import CometidoTable

# Create your views here.
from .forms import CometidoForm, DestinoForm #,DestinoFormSet
from .models import Cometido, Destino
from personas.models import *
from django.views.generic import CreateView


@login_required
def cometido_create(request):

	form = CometidoForm(request.POST or None)

	if form.is_valid():
		persona = Persona.objects.get(pk=request.user)
		instance = form.save(commit=False)
		instance.rut = persona.rut
                instance.persona = request.user
                instance.save()
		#formset = DestinoFormSet(request.POST or None,request.FILES,instance=instance)
		#if formset.is_valid():
            	#formset.save(commit=False)
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
                #formset = DestinoFormSet()
	context = {
		"form": form,
		#"formset": formset,
	}
	return render(request, "cometidos/cometido_form.html", context)

@login_required
def cometido_detail(request, id=None):
	instance = get_object_or_404(Cometido, id=id)
	if instance.derechoaviatico:
		instance.derechoaviatico = 'Si'
	else:
		instance.derechoaviatico = 'No'	
	if instance.convocadopor == 'NC':
		instance.convocadopor = 'Nivel Central'
	if instance.convocadopor == 'NR':
		instance.convocadopor = 'Nivel Regional'
	context = {
		"title": "Detalle",
		"instance": instance,
	}
	return render(request, "cometidos/cometido_detail.html", context)


@login_required
def cometido_list(request):
	#queryset = Cometido.objects.all()
	queryset = Cometido.objects.filter(persona=Persona.objects.get(pk=request.user))
	#cant = queryset.count()
	#print queryset
	example2 = CometidoTable(queryset, prefix="5-")
	RequestConfig(request, paginate={"per_page": 10}).configure(example2)

	context = {
		"object_list": queryset,
		"title": "Lista Cometidos",
		"example2": example2,
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
	return render(request, "cometidos/cometido_form.html", context)


def cometido_delete(request):
	return HttpResponse("<h1>Borrar Cometidos<h1>")
