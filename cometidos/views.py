from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig, SingleTableView
from .tables import CometidoTable
from datetime import datetime

# Create your views here.
from .forms import CometidoForm, DestinoForm #,DestinoFormSet
from .models import Cometido, Destino
from personas.models import *
from django.views.generic import CreateView

from .report_class import CjReport
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
#from reportlab.platypus.tables import Table
from establecimientos.models import *
from .forms import *



@login_required
def cometido_create(request):

	formCometido = CometidoForm(request.POST or None)
	formDestino = DestinoForm()
	if formCometido.is_valid():
		persona = Persona.objects.get(pk=request.user)
		instance = formCometido.save(commit=False)
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
		formCometido = CometidoForm(initial=data)
	context = {
		"form": formCometido,
		"destino": formDestino,
	}
	return render(request, "cometidos/cometido_form.html", context)

@login_required
def cometido_detail(request, id=None):
	instance = get_object_or_404(Cometido, id=id, persona=request.user)
	instance.derechoaviatico = convierteBooleanString(instance.derechoaviatico)
	instance.convocadopor = convocadopor(instance.convocadopor)
	if instance.financiagastosde:
		for indice in range(len(instance.financiagastosde)):
			instance.financiagastosde[indice]=financiagastosde(instance.financiagastosde[indice])
	else:	
		instance.financiagastosde=financiagastosde(instance.financiagastosde)
	instance.viaaerea = convierteBooleanString(instance.viaaerea)
	instance.viaffcc = convierteBooleanString(instance.viaffcc)
	instance.viabus = convierteBooleanString(instance.viabus)
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


@login_required
def cometido_print(request, id=None):
	instance = get_object_or_404(Cometido, id=id, persona=request.user)
	cometido  = Cometido.objects.get(id=id)
	if cometido.financiagastosde:
		for indice in range(len(cometido.financiagastosde)):
			cometido.financiagastosde[indice]=financiagastosde(cometido.financiagastosde[indice])
	else:	
		cometido.financiagastosde=financiagastosde(cometido.financiagastosde)
	if cometido.diadesalida is not None:
		cometido.diadesalida =datetime.strptime(str(cometido.diadesalida),'%Y-%m-%d').strftime('%d-%m-%Y')
	if cometido.horadesalida is not None:
		cometido.horadesalida = datetime.strptime(str(cometido.horadesalida),'%H:%M:%S').strftime('%H:%M')
	if cometido.diadellegada is not None:
		cometido.diadellegada = datetime.strptime(str(cometido.diadellegada),'%Y-%m-%d').strftime('%d-%m-%Y')
	if cometido.horadellegada is not None:
		cometido.horadellegada = datetime.strptime(str(cometido.horadellegada),'%H:%M:%S').strftime('%H:%M')
        data = {
		'rut': cometido.rut,
                'nombre': request.user.first_name + ' ' + request.user.last_name,
                'grado': cometido.grado,
                'escalafon': cometido.escalafon,
                'estamento': cometido.estamento,
                'unidad': cometido.unidad,
                'region': cometido.region,
		'convocadopor': convocadopor(cometido.convocadopor),
		'financiagastosde': cometido.financiagastosde,
		'al100': cometido.al100,
		'al60': cometido.al60,
		'al50': cometido.al50,
		'al40': cometido.al40,
		'derechoaviatico': convierteBooleanString(cometido.derechoaviatico),
		'diadesalida': cometido.diadesalida,
		'horadesalida': cometido.horadesalida,
		'diadellegada': cometido.diadellegada,
		'horadellegada': cometido.horadellegada,
                }
	response = HttpResponse(content_type='application/pdf')
	filename = 'Cometido_'+id+'.pdf'
	response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
	logo = 'static/img/logo.png'
	font="Helvetica"
	font_bold = "Helvetica-Bold"
	size_font = 12
	p = canvas.Canvas(response)
	p.setStrokeColorRGB(0,0,0)
	p.drawImage(logo,1*cm,26*cm,5*cm,2.5*cm)
        
	p.setFont(font_bold, 14)
        p.drawString(2.3*cm,25*cm,"SOLICITUD DE COMETIDOS Y COMISIONES DE SERVICIO Nro  " + id )
        
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,24*cm,"I.- IDENTIFICACION" )
        
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,23*cm,"Nombre Completo" )
	p.setFont(font, size_font)
        p.drawString(5.5*cm,23*cm,data['nombre'] )
        p.line(5.5*cm,22.9*cm,18*cm,22.9*cm)
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,22.3*cm,"Rut")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,22.3*cm,data['rut'])
        p.line(5.5*cm,22.2*cm,8.5*cm,22.2*cm)
	p.setFont(font_bold, size_font)
        p.drawString(9*cm,22.3*cm,"Grado")
	p.setFont(font, size_font)
        p.drawString(10.7*cm,22.3*cm,data['grado'])
        p.line(10.5*cm,22.2*cm,11.5*cm,22.2*cm)
	p.setFont(font_bold, size_font)
        p.drawString(12*cm,22.3*cm,"Estamento")
	p.setFont(font, size_font)
        p.drawString(14.8*cm,22.3*cm,data['estamento'])
        p.line(14.5*cm,22.2*cm,18*cm,22.2*cm)
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,21.6*cm,"Calidad Juridica")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,21.6*cm,data['escalafon'])
        p.line(5.5*cm,21.5*cm,18*cm,21.5*cm)
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,20.9*cm,"Dependencia")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,20.9*cm,"Unidad de ")
	p.setFont(font, size_font)
        p.drawString(7.5*cm,20.9*cm,data['unidad'])
	p.setFont(font_bold, size_font)
        p.line(5.5*cm,20.8*cm,10.5*cm,20.8*cm)
        p.drawString(10.7*cm,20.9*cm,"Direccion ")
	p.setFont(font, size_font)
        p.drawString(12.7*cm,20.9*cm,data['region'])
        p.line(12.7*cm,20.8*cm,18*cm,20.8*cm)
        #Titulo ESPECIFICACION
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,20*cm,"II.- ESPECIFICACION" )
        


	#Titulo INFORMACION ADICIONAL
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,14*cm,"III.- INFORMACION ADICIONAL" )
        p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,13.3*cm,"Convocado por" )
        p.setFont(font,size_font)
        p.drawString(5.5*cm,13.3*cm,data['convocadopor'] )
        p.line(5.5*cm,13.2*cm,18*cm,13.2*cm)
	#Financia Gastos de
        p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,12.7*cm,"Financia gastos de" )
        p.setFont(font, size_font)
	x = 5.5
	for i in range(len(cometido.financiagastosde)):
        	p.drawString(x*cm,12.7*cm,cometido.financiagastosde[i])
		x = x + 2.8
        p.line(5.5*cm,12.6*cm,18*cm,12.6*cm)
	#Subtitulo VIATICOS
        p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,12*cm,"Viaticos" )
	#Dias al 100        
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,11.3*cm,"Dias al 100%" )
        p.setFont(font, size_font)
        p.drawString(5.5*cm,11.3*cm,str(data['al100']))
        p.line(5.2*cm,11.2*cm,6.3*cm,11.2*cm)
        #Dias al 60
	p.setFont(font_bold, size_font)
        p.drawString(6.6*cm,11.3*cm,"Dias al 60%" )
        p.setFont(font, size_font)
        p.drawString(9.3*cm,11.3*cm,str(data['al60']))
        p.line(9*cm,11.2*cm,10*cm,11.2*cm)
	#Dias al 50
	p.setFont(font_bold, size_font)
        p.drawString(10.6*cm,11.3*cm,"Dias al 50%" )
        p.setFont(font, size_font)
        p.drawString(13.3*cm,11.3*cm,str(data['al50']))
        p.line(13*cm,11.2*cm,14*cm,11.2*cm)
	#Dias al 40
	p.setFont(font_bold, size_font)
        p.drawString(14.6*cm,11.3*cm,"Dias al 40%" )
        p.setFont(font, size_font)
        p.drawString(17.3*cm,11.3*cm,str(data['al40']))
        p.line(17*cm,11.2*cm,18*cm,11.2*cm)
	#Con derecho a viatico
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,10.7*cm,"Con derecho a viatico" )
	p.setFont(font, size_font)
        p.drawString(7.8*cm,10.7*cm,data['derechoaviatico'] )
        p.line(7.2*cm,10.6*cm,18*cm,10.6*cm)
	#Dia de Salida
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,10*cm,"Dia de salida" )
        p.setFont(font, size_font)
        p.drawString(6.3*cm,10*cm,str(data['diadesalida']))
        p.line(5.5*cm,9.9*cm,9.5*cm,9.9*cm)
	#Hora de Salida
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,10*cm,"Hora de salida" )
        p.setFont(font, size_font)
        p.drawString(14.5*cm,10*cm,str(data['horadesalida']))
        p.line(13.5*cm,9.9*cm,18*cm,9.9*cm)
	#Dia de llegada
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,9.4*cm,"Dia de llegada" )
        p.setFont(font, size_font)
        p.drawString(6.3*cm,9.4*cm,str(data['diadellegada']))
        p.line(5.5*cm,9.3*cm,9.5*cm,9.3*cm)
	#Hora de llegada
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,9.4*cm,"Hora de llegada" )
        p.setFont(font, size_font)
        p.drawString(14.5*cm,9.4*cm,str(data['horadellegada']))
        p.line(13.5*cm,9.3*cm,18*cm,9.3*cm)
	#Subtitulo MEDIOS DE TRANSPORTE
        p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,8.7*cm,"Medio de transporte a utilizar para el viatico" )
	

	p.showPage()
	p.save()
	return response


def convocadopor(self):
	switcher = {
		'NR': 'Nivel Regional',
		'NC': 'Nivel Central',
		'OT': 'Otro'
	}
	return switcher.get(self,'--')

def financiagastosde(self):
	switcher = {
		'AJ': 'Alojamiento',
		'AM': 'Alimentacion',
	}
	return switcher.get(self,'Ninguno')	
	

def convierteBooleanString(self):
	if self:
		return 'Si'
	else:
		return 'No'
		
