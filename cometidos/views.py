from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def cometido_create(request):
	return HttpResponse("<h1>Crea Cometido<h1>")

def cometido_detail(request):
	return HttpResponse("<h1>Detalle Cometido<h1>")

def cometido_list(request):
	return HttpResponse("<h1>Listar Cometidos<h1>")

def cometido_update(request):
	return HttpResponse("<h1>Actualizar Cometidos<h1>")

def cometido_delete(request):
	return HttpResponse("<h1>Borrar Cometidos<h1>")
