# -*- coding: utf-8 -*-
from io import BytesIO

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig, SingleTableView
from datetime import datetime
from django.views.generic import CreateView, ListView

# Create your views here.
from .forms import CometidoForm, DestinoForm #,DestinoFormSet
from .models import Cometido, Destino
from personas.models import *
from establecimientos.models import *


from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table,Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, legal
from reportlab.lib.enums import TA_LEFT, TA_CENTER,TA_JUSTIFY
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas



@login_required
def cometido_create(request):
	formCometido = CometidoForm(request.POST or None)
	formDestino = DestinoForm()
	persona = Persona.objects.get(pk=request.user)
	if formCometido.is_valid():
		instance = formCometido.save(commit=False)
		instance.rut = persona.rut
                instance.persona = request.user
                instance.save()
		formCometido.save_m2m()
                messages.success(request, 'Cometido creado satisfactoriamente')
                return HttpResponseRedirect(instance.get_absolute_url())
	else:
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
	conductor = False
	if persona.actividad.nombre == 'Conductor':
		conductor = True
	context = {
		"form": formCometido,
		"destino": formDestino,
		"conductor": conductor,
	}
	return render(request, "cometidos/form.html", context)

@login_required
def cometido_detail(request, id=None):
	instance = get_object_or_404(Cometido, id=id, persona=request.user)
	persona = Persona.objects.get(pk=request.user)
	instance.derechoaviatico = convierteBooleanString(instance.derechoaviatico)
	instance.convocadopor = convocadopor(instance.convocadopor)
	tipofinanciamiento = instance.tipofinanciamiento.all()
	instance.viaaerea = convierteBooleanString(instance.viaaerea)
	instance.viaffcc = convierteBooleanString(instance.viaffcc)
	instance.viabus = convierteBooleanString(instance.viabus)
	instance.viavehiculofiscal = convierteBooleanString(instance.viavehiculofiscal)
	instance.viavehiculoparticular = convierteBooleanString(instance.viavehiculoparticular)
	instance.viataxitransfers = convierteBooleanString(instance.viataxitransfers)
	instance.viamaritima = convierteBooleanString(instance.viamaritima)
	#instance.diadesalida = encasodevalorvacio(instance.diadesalida)
	instance.horadesalida = encasodevalorvacio(instance.horadesalida)
	instance.diadellegada = encasodevalorvacio(instance.diadellegada)
	instance.horadellegada = encasodevalorvacio(instance.horadellegada)
	conductor = False
	if persona.actividad.nombre=='Conductor':
		conductor = True
	context = {
		"title": "Detalle",
		"instance": instance,
		"conductor": conductor,
		"tipofinanciamiento": tipofinanciamiento,
	}
	return render(request, "cometidos/detail.html", context)


@login_required
def cometido_list(request):
	queryset = Cometido.objects.filter(persona=Persona.objects.get(pk=request.user))
	context = {
		"object_list": queryset,
		"title": "Lista Cometidos",
	}
	return render(request, "cometidos/index.html", context)

@login_required
def cometido_update(request, id=None):
	instance = get_object_or_404(Cometido, id=id,persona=request.user)
	form = CometidoForm(request.POST or None, instance=instance)
	persona = Persona.objects.get(pk=request.user)
        if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
		form.save_m2m()
                messages.success(request, 'Cometido actualizado satisfactoriamente')
                return HttpResponseRedirect(instance.get_absolute_url())
	conductor = False
	if persona.actividad.nombre=='Conductor':
		conductor = True
	context = {
		"instance": instance,
		"form": form,
		'conductor': conductor,
	}
	return render(request, "cometidos/form.html", context)


def cometido_delete(request):
	return HttpResponse("<h1>Borrar Cometidos<h1>")


@login_required
def cometido_print(request, id=None):
	instance = get_object_or_404(Cometido, id=id, persona=request.user)
	tipofinanciamiento = instance.tipofinanciamiento.all()
	cometido  = Cometido.objects.get(id=id)
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
		'financiagastosde': tipofinanciamiento,
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
	p = canvas.Canvas(response,pagesize=legal)


	p.setStrokeColorRGB(0,0,0)
	p.drawImage(logo,1*cm,32*cm,5*cm,2.5*cm)
        
	p.setFont(font_bold, 14)
        p.drawString(2.3*cm,31*cm,"SOLICITUD DE COMETIDOS Y COMISIONES DE SERVICIO Nro  " + id )
        
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,30*cm,"I.- IDENTIFICACION" )
        
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,29*cm,"Nombre Completo" )
	p.setFont(font, size_font)
        p.drawString(5.5*cm,29*cm,data['nombre'] )
        p.line(5.5*cm,28.9*cm,18*cm,28.9*cm)
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,28.3*cm,"Rut")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,28.3*cm,data['rut'])
        p.line(5.5*cm,28.2*cm,8.5*cm,28.2*cm)
	p.setFont(font_bold, size_font)
        p.drawString(9*cm,28.3*cm,"Grado")
	p.setFont(font, size_font)
        p.drawString(10.7*cm,28.3*cm,data['grado'])
        p.line(10.5*cm,28.2*cm,11.5*cm,28.2*cm)
	p.setFont(font_bold, size_font)
        p.drawString(12*cm,28.3*cm,"Estamento")
	p.setFont(font, size_font)
        p.drawString(14.8*cm,28.3*cm,data['estamento'])
        p.line(14.5*cm,28.2*cm,18*cm,28.2*cm)
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,27.6*cm,"Calidad Juridica")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,27.6*cm,data['escalafon'])
        p.line(5.5*cm,27.5*cm,18*cm,27.5*cm)
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,26.9*cm,"Dependencia")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,26.9*cm,"Unidad de ")
	p.setFont(font, size_font)
        p.drawString(7.5*cm,26.9*cm,data['unidad'])
	p.setFont(font_bold, size_font)
        p.line(5.5*cm,26.8*cm,10.5*cm,26.8*cm)
        p.drawString(10.7*cm,26.9*cm,"Direccion ")
	p.setFont(font, size_font)
        p.drawString(12.7*cm,26.9*cm,data['region'])
        p.line(12.7*cm,26.8*cm,18*cm,26.8*cm)
        #Titulo ESPECIFICACION
	p.setFont(font_bold, size_font)
        p.drawString(1.5*cm,26*cm,"II.- ESPECIFICACION" )
        


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
	for i in tipofinanciamiento:
        	p.drawString(x*cm,12.7*cm,i.nombre)
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

	#if cometido.viaaerea:
		 	

	p.showPage()
	p.save()
	return response


def convocadopor(self):
	switcher = {
		'NR': 'Nivel Regional',
		'NC': 'Nivel Central',
		'OT': 'Otro'
	}
	return switcher.get(self,'---')

def financiagastosde(self):
	switcher = {
		'AJ': 'Alojamiento',
		'AM': 'Alimentacion',
	}
	return switcher.get(self,'---')	
	

def convierteBooleanString(self):
	if self:
		return 'Si'
	else:
		return 'No'
	

def encasodevalorvacio(self):
	if self:
		return '---'
	else:
		return self


class IndexView(ListView):
	template_name = "cometidos/print.html"
	model = Cometido
	context_object_name =  "c"

def generar_pdf(request, id=None):
	response = HttpResponse(content_type='application/pdf')
	pdf_name = "Cometido.pdf"
	response['Content-Disposition']= 'attachment; filename=%s' % pdf_name
	buff = BytesIO()
	doc = SimpleDocTemplate(buff, pagesizes=letter, rightMargin=40, leftMargin=60, topMargin=60, bottonMargin=18,)
	cometidos = []
	styles = getSampleStyleSheet()
	#styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	header = Paragraph("Listado de Cometidos", styles['Heading1'])
	cometidos.append(header)
	headings = ('Num','Rut','Nombre','Grado')
	allcometidos = [(p.id,p.rut, p.nombre, p.grado ) for p in Cometido.objects.all()]
#	print allcometidos

	t =  Table([headings] + allcometidos)
	t.setStyle(TableStyle(
		[
			('GRID', (0,0), (3,-1),1,colors.dodgerblue),
			('LINEBELOW',(0,0),(-1,0),2,colors.darkblue),
			('BACKGROUND',(0,0),(-1,0),colors.dodgerblue)
		]
	))
	cometidos.append(t)
	Story=[]
	logo = "static/img/logo.png"

	# We really want to scale the image to fit in a box and keep proportions.
	im = Image(logo, 1*cm, 2.5*cm)
	cometidos.append(im)

	ptext = '<font size=12>Some text</font>' 
	cometidos.append(Paragraph(ptext, styles["Normal"]))

	ptext = '''
	<seq>. </seq>Some Text<br/>
	<seq>. </seq>Some more test Text
	'''
	cometidos.append(Paragraph(ptext, styles["Bullet"]))
	
	ptext='<bullet>&bull;</bullet>Some Text'
	cometidos.append(Paragraph(ptext, styles["Bullet"]))

	logo = 'static/img/logo.png'
        font="Helvetica"
        font_bold = "Helvetica-Bold"
        size_font = 12
        p = canvas.Canvas(response)
        p.setStrokeColorRGB(0,0,0)
        p.drawImage(logo,1*cm,26*cm,5*cm,2.5*cm)

	
	#doc.build(Story)
	doc.build(cometidos)
	response.write(buff.getvalue())
	buff.close()
	p.save()
	return response
	
