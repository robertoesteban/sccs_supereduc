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
	instance.gastoscombustiblepeaje = convierteBooleanString(instance.gastoscombustiblepeaje)
	instance.gastosmovilizacion = convierteBooleanString(instance.gastosmovilizacion)
	instance.gastosenvehiculoparticular = convierteBooleanString(instance.gastosenvehiculoparticular)
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
	persona = Persona.objects.get(pk=request.user)
	if instance.diadesalida is not None:
		instance.diadesalida =datetime.strptime(str(instance.diadesalida),'%Y-%m-%d').strftime('%d-%m-%Y')
	if instance.horadesalida is not None:
		instance.horadesalida = datetime.strptime(str(instance.horadesalida),'%H:%M:%S').strftime('%H:%M')
	if instance.diadellegada is not None:
		instance.diadellegada = datetime.strptime(str(instance.diadellegada),'%Y-%m-%d').strftime('%d-%m-%Y')
	if instance.horadellegada is not None:
		instance.horadellegada = datetime.strptime(str(instance.horadellegada),'%H:%M:%S').strftime('%H:%M')
	response = HttpResponse(content_type='application/pdf')
	filename = 'Cometido_'+id+'.pdf'
	response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
	logo = 'static/img/logo.png'
	font="Helvetica"
	font_bold = "Helvetica-Bold"
	size_font = 10
	p = canvas.Canvas(response,pagesize=legal)


	p.setStrokeColorRGB(0,0,0)
	p.drawImage(logo,1*cm,32*cm,5*cm,2.5*cm)
        
	p.setFont(font_bold, 14)
        p.drawString(2.3*cm,31*cm,"SOLICITUD DE COMETIDOS Y COMISIONES DE SERVICIO Nro  " + id )
        IDEN=0.7
	p.setFont(font_bold, size_font)
        p.drawString(2*cm,(29.6+IDEN)*cm,"I.- IDENTIFICACION" )
	p.setFont(font_bold, size_font)
        p.drawString(2*cm,(29+IDEN)*cm,"Nombre Completo" )
	p.setFont(font, size_font)
        p.drawString(5.5*cm,(29+IDEN)*cm,request.user.first_name + ' ' + request.user.last_name)
        p.line(5.5*cm,(28.9+IDEN)*cm,19*cm,(28.9+IDEN)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(2*cm,(28.3+IDEN)*cm,"Rut")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,(28.3+IDEN)*cm,instance.rut)
        p.line(5.5*cm,(28.2+IDEN)*cm,8.5*cm,(28.2+IDEN)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(9*cm,(28.3+IDEN)*cm,"Grado")
	p.setFont(font, size_font)
        p.drawString(10.7*cm,(28.3+IDEN)*cm,instance.grado)
        p.line(10.5*cm,(28.2+IDEN)*cm,11.5*cm,(28.2+IDEN)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(12*cm,(28.3+IDEN)*cm,"Estamento")
	p.setFont(font, size_font)
        p.drawString(14.8*cm,(28.3+IDEN)*cm,instance.estamento)
        p.line(14.5*cm,(28.2+IDEN)*cm,19*cm,(28.2+IDEN)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(2*cm,(27.6+IDEN)*cm,"Calidad Jurídica")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,(27.6+IDEN)*cm,instance.escalafon)
        p.line(5.5*cm,(27.5+IDEN)*cm,19*cm,(27.5+IDEN)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(2*cm,(26.9+IDEN)*cm,"Dependencia")
	p.setFont(font, size_font)
        p.drawString(5.5*cm,(26.9+IDEN)*cm,"Unidad de")
	p.setFont(font, size_font)
        p.drawString(7.3*cm,(26.9+IDEN)*cm,instance.unidad)
	p.setFont(font_bold, size_font)
        p.line(5.5*cm,(26.8+IDEN)*cm,10.5*cm,(26.8+IDEN)*cm)
        p.drawString(10.7*cm,(26.9+IDEN)*cm,"Dirección")
	p.setFont(font, size_font)
        p.drawString(12.7*cm,(26.9+IDEN)*cm,instance.region)
        p.line(12.7*cm,(26.8+IDEN)*cm,19*cm,(26.8+IDEN)*cm)
        
	ESPE=0.7
	#Titulo ESPECIFICACION
	p.setFont(font_bold, size_font)
        p.drawString(2*cm,(26+ESPE)*cm,"II.- ESPECIFICACION" )
        



	INFO=2
	#Titulo INFORMACION ADICIONAL
	p.setFont(font_bold, size_font)
        p.drawString(2*cm,(20.4+INFO)*cm,"III.- INFORMACION ADICIONAL" )
        p.setFont(font_bold, size_font)
        p.drawString(2*cm,(19.8+INFO)*cm,"Convocado por" )
        p.setFont(font,size_font)
        p.drawString(5.5*cm,(19.8+INFO)*cm,convocadopor(instance.convocadopor))
        p.line(5.5*cm,(19.7+INFO)*cm,19*cm,(19.7+INFO)*cm)
	#Financia Gastos de
        p.setFont(font_bold, size_font)
        p.drawString(2*cm,(19.2+INFO)*cm,"Financia gastos de" )
        p.setFont(font, size_font)
	x = 5.5
	for i in tipofinanciamiento:
        	p.drawString(x*cm,(19.2+INFO)*cm,i.nombre)
		x = x + 2.8
        p.line(5.5*cm,(19.1+INFO)*cm,19*cm,(19.1+INFO)*cm)
	#Subtitulo VIATICOS
        p.setFont(font_bold, size_font)
        p.drawString(2*cm,(18.5+INFO)*cm,"Viáticos")
	#Con derecho a viatico
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(17.9+INFO)*cm,"Con derecho a viático")
	p.setFont(font, size_font)
        p.drawString(8*cm,(17.9+INFO)*cm,convierteBooleanString(instance.derechoaviatico))
        p.line(7.5*cm,(17.8+INFO)*cm,9.5*cm,(17.8+INFO)*cm)
	#Dias al 100        
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(17.3+INFO)*cm,"Días al 100%" )
        p.setFont(font, size_font)
        p.drawString(5.5*cm,(17.3+INFO)*cm,str(instance.al100))
        p.line(5.2*cm,(17.2+INFO)*cm,6.3*cm,(17.2+INFO)*cm)
        #Dias al 60
	p.setFont(font_bold, size_font)
        p.drawString(6.6*cm,(17.3+INFO)*cm,"Días al 60%" )
        p.setFont(font, size_font)
        p.drawString(9.3*cm,(17.3+INFO)*cm,str(instance.al60))
        p.line(9*cm,(17.2+INFO)*cm,10*cm,(17.2+INFO)*cm)
	#Dias al 50
	p.setFont(font_bold, size_font)
        p.drawString(10.6*cm,(17.3+INFO)*cm,"Días al 50%" )
        p.setFont(font, size_font)
        p.drawString(13.3*cm,(17.3+INFO)*cm,str(instance.al50))
        p.line(13*cm,(17.2+INFO)*cm,14*cm,(17.2+INFO)*cm)
	#Dias al 40
	p.setFont(font_bold, size_font)
        p.drawString(14.6*cm,(17.3+INFO)*cm,"Días al 40%" )
        p.setFont(font, size_font)
        p.drawString(17.4*cm,(17.3+INFO)*cm,str(instance.al40))
        p.line(17*cm,(17.2+INFO)*cm,19*cm,(17.2+INFO)*cm)
	#Dia de Salida
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(16.7+INFO)*cm,"Día de salida" )
        p.setFont(font, size_font)
        p.drawString(6.3*cm,(16.7+INFO)*cm,str(instance.diadesalida))
        p.line(5.5*cm,(16.6+INFO)*cm,9.5*cm,(16.6+INFO)*cm)
	#Hora de Salida
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,(16.7+INFO)*cm,"Hora de salida" )
        p.setFont(font, size_font)
        p.drawString(14.5*cm,(16.7+INFO)*cm,str(instance.horadesalida))
        p.line(13.5*cm,(16.6+INFO)*cm,19*cm,(16.6+INFO)*cm)
	#Dia de llegada
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(16.1+INFO)*cm,"Día de llegada" )
        p.setFont(font, size_font)
        p.drawString(6.3*cm,(16.1+INFO)*cm,str(instance.diadellegada))
        p.line(5.5*cm,(16+INFO)*cm,9.5*cm,(16+INFO)*cm)
	#Hora de llegada
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,(16.1+INFO)*cm,"Hora de llegada" )
        p.setFont(font, size_font)
        p.drawString(14.5*cm,(16.1+INFO)*cm,str(instance.horadellegada))
        p.line(13.5*cm,(16+INFO)*cm,19*cm,(16+INFO)*cm)
	#Subtitulo MEDIOS DE TRANSPORTE
        p.setFont(font_bold, size_font)
        p.drawString(2*cm,(15.5+INFO)*cm,"Medio de transporte a utilizar para el cometido")

	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(14.9+INFO)*cm,"Vía Aérea")
        p.setFont(font, size_font)
        p.drawString(8*cm,(14.9+INFO)*cm,str(convierteBooleanString(instance.viaaerea)))
        p.line(7.5*cm,(14.8+INFO)*cm,9.5*cm,(14.8+INFO)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,(14.9+INFO)*cm,"Línea Aérea")
        p.setFont(font, size_font)
        p.drawString(14.5*cm,(14.9+INFO)*cm,str(instance.lineaaerea))
        p.line(13.5*cm,(14.8+INFO)*cm,19*cm,(14.8+INFO)*cm)
		 	
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(14.3+INFO)*cm,"Vía FFCC" )
        p.setFont(font, size_font)
        p.drawString(8*cm,(14.3+INFO)*cm,str(convierteBooleanString(instance.viaffcc)))
        p.line(7.5*cm,(14.2+INFO)*cm,9.5*cm,(14.2+INFO)*cm)

	
	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(13.7+INFO)*cm,"Vía Bus" )
        p.setFont(font, size_font)
        p.drawString(8*cm,(13.7+INFO)*cm,str(convierteBooleanString(instance.viabus)))
        p.line(7.5*cm,(13.6+INFO)*cm,9.5*cm,(13.6+INFO)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,(13.7+INFO)*cm,"Empresa de Bus" )
        p.setFont(font, size_font)
        p.drawString(14.5*cm,(13.7+INFO)*cm,str(instance.lineabus))
        p.line(13.5*cm,(13.6+INFO)*cm,19*cm,(13.6+INFO)*cm)

	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(13.1+INFO)*cm,"Vía vehículo fiscal")
        p.setFont(font, size_font)
        p.drawString(8*cm,(13.1+INFO)*cm,str(convierteBooleanString(instance.viavehiculofiscal)))
        p.line(7.5*cm,(13+INFO)*cm,9.5*cm,(13+INFO)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,(13.1+INFO)*cm,"Vehículo Fiscal" )
        p.setFont(font, size_font)
        p.drawString(14.5*cm,(13.1+INFO)*cm,str(instance.vehiculofiscal))
        p.line(13.5*cm,(13+INFO)*cm,19*cm,(13+INFO)*cm)


	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(12.5+INFO)*cm,"Vía vehículo particular")
        p.setFont(font, size_font)
        p.drawString(8*cm,(12.5+INFO)*cm,str(convierteBooleanString(instance.viavehiculoparticular)))
        p.line(7.5*cm,(12.4+INFO)*cm,9.5*cm,(12.4+INFO)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,(12.5+INFO)*cm,"Placa Patente" )
        p.setFont(font, size_font)
        p.drawString(14.5*cm,(12.5+INFO)*cm,str(instance.placapatente))
        p.line(13.5*cm,(12.4+INFO)*cm,19*cm,(12.4+INFO)*cm)

	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(11.9+INFO)*cm,"Vía Taxi o Transfer" )
        p.setFont(font, size_font)
        p.drawString(8*cm,(11.9+INFO)*cm,convierteBooleanString(instance.viataxitransfers))
        p.line(7.5*cm,(11.8+INFO)*cm,9.5*cm,(11.8+INFO)*cm)


	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(11.3+INFO)*cm,"Vía Marítima")
        p.setFont(font, size_font)
        p.drawString(8*cm,(11.3+INFO)*cm,convierteBooleanString(instance.viamaritima))
        p.line(7.5*cm,(11.2+INFO)*cm,9.5*cm,(11.2+INFO)*cm)


	#Subtitulo GASTOS ESTIMADOS
        p.setFont(font_bold, size_font)
        p.drawString(2*cm,(10.7+INFO)*cm,"Gastos estimados a ejecutar durante el cometido" )

	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(10.1+INFO)*cm,"Combustible - Peaje" )
        p.setFont(font, size_font)
        p.drawString(8*cm,(10.1+INFO)*cm,convierteBooleanString(instance.gastoscombustiblepeaje))
        p.line(7.5*cm,(10+INFO)*cm,9.5*cm,(10+INFO)*cm)

	p.setFont(font_bold, size_font)
        p.drawString(2.6*cm,(9.5+INFO)*cm,"Gastos de Movilización" )
        p.setFont(font, size_font)
        p.drawString(8*cm,(9.5+INFO)*cm,convierteBooleanString(instance.gastosmovilizacion))
        p.line(7.5*cm,(9.4+INFO)*cm,9.5*cm,(9.4+INFO)*cm)
	p.setFont(font_bold, size_font)
        p.drawString(10*cm,(9.5+INFO)*cm,"Vehículo Particular" )
        p.setFont(font, size_font)
        p.drawString(15.5*cm,(9.5+INFO)*cm,convierteBooleanString(instance.gastosenvehiculoparticular))
        p.line(14*cm,(9.4+INFO)*cm,19*cm,(9.4+INFO)*cm)
	x=1.4
	if persona.actividad.nombre=='Conductor':
		#Subtitulo SOLO PARA CONDUCTORES
        	p.setFont(font_bold, size_font)
        	p.drawString(2*cm,(8.8+INFO)*cm,"Solo aplica para el caso de ser conductor")

		p.setFont(font_bold, size_font)
        	p.drawString(2.6*cm,(8.2+INFO)*cm,"Km inicial Real")
        	p.setFont(font, size_font)
        	p.drawString(8*cm,(8.2+INFO)*cm,str(instance.kminicial))
        	p.line(7.5*cm,(8.1+INFO)*cm,9.5*cm,(8.1+INFO)*cm)
		p.setFont(font_bold, size_font)
        	p.drawString(10*cm,(8.2+INFO)*cm,"Km final Estimado" )
        	p.setFont(font, size_font)
        	p.drawString(15.5*cm,(8.2+INFO)*cm,str(instance.kmfinal))
        	p.line(14*cm,(8.1+INFO)*cm,19*cm,(8.1+INFO)*cm)
		x=0
	

	p.line(1.5*cm,(7.6+x+INFO)*cm,19.5*cm,(7.6+x+INFO)*cm)
	p.line(1.5*cm,(4.6+x+INFO)*cm,19.5*cm,(4.6+x+INFO)*cm)
	p.line(1.5*cm,(3.6+x+INFO)*cm,19.5*cm,(3.6+x+INFO)*cm)
	p.line(1.5*cm,(7.6+x+INFO)*cm,1.5*cm,(3.6+x+INFO)*cm)
	p.line(19.5*cm,(7.6+x+INFO)*cm,19.5*cm,(3.6+x+INFO)*cm)
	p.line(10.5*cm,(7.6+x+INFO)*cm,10.5*cm,(3.6+x+INFO)*cm)
	p.line(6*cm,(7.6+x+INFO)*cm,6*cm,(3.6+x+INFO)*cm)
	p.line(15*cm,(7.6+x+INFO)*cm,15*cm,(3.6+x+INFO)*cm)
	p.setFont(font, 8)
        p.drawString(2.4*cm,(4.1+x+INFO)*cm,"Firma Funcionario" )
        p.drawString(7.3*cm,(4.2+x+INFO)*cm,"Firma y Timbre")
        p.drawString(7.2*cm,(3.8+x+INFO)*cm,"Jefatura Directa" )
        p.drawString(11.8*cm,(4.2+x+INFO)*cm,"Firma y Timbre")
        p.drawString(10.9*cm,(3.8+x+INFO)*cm,"Coordinadora Administración" )
        p.drawString(16.3*cm,(4.2+x+INFO)*cm,"Firma y Timbre")
        p.drawString(16.2*cm,(3.8+x+INFO)*cm,"Director Regional" )
	
	
        p.setFont(font_bold, size_font)
        p.drawString(2*cm,(2.6+x+INFO)*cm,"Observaciones")
        p.setFont(font, size_font)
        p.drawString(5.2*cm,(2.6+x+INFO)*cm,str(instance.observaciones))
	p.line(5.2*cm,(2.5+x+INFO)*cm,19*cm,(2.5+x+INFO)*cm)
	

	
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
		return 'Sí'
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
	
