# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from personas.models import *
from territorios.models import *
from establecimientos.models import *
from mediosdetransporte.models import *
from django.utils import timezone
from django.core.urlresolvers import reverse
from django import forms
from multiselectfield import MultiSelectField

# Create your models here.

OPCIONES_CONVOCADOPOR = (
        ('NR','Nivel Regional'),
        ('NC','Nivel Central'),
	('OT','Otro')
        )


OPCIONES_FINANCIAGASTOSDE = (
        ('AJ','Alojamiento'),
        ('AM','Alimentacion'),
        )

class Cometido(models.Model):
	rut = models.CharField("Rut",max_length=12,blank=False,null=False)
	nombre = models.CharField("Nombre Completo", max_length=180, blank=False, null=False)
	persona = models.ForeignKey(settings.AUTH_USER_MODEL, default=User)
	grado = models.CharField("Grado",max_length=60,blank=False,null=False)
	escalafon = models.CharField("Escalafon",max_length=60,blank=False,null=False)
	estamento = models.CharField("Estamento",max_length=60,blank=False,null=False)
	unidad = models.CharField("Unidad",max_length=60,blank=False,null=False)
	region = models.CharField("Región",max_length=60,blank=False,null=False)
	convocadopor = models.CharField("Convocado por", max_length=2, choices=OPCIONES_CONVOCADOPOR,blank=True, null=True)
	financiagastosde = MultiSelectField(choices=OPCIONES_FINANCIAGASTOSDE,blank=True, null=True,verbose_name='Financia Gastos de')
	derechoaviatico = models.BooleanField("Con derecho a viático",default=False) 
	diadesalida = models.DateField("Día de salida",blank=True, null=True)
	horadesalida = models.TimeField("Hora de salida",blank=True, null=True)
	diadellegada = models.DateField("Día de llegada",blank=True, null=True)
	horadellegada = models.TimeField("Hora de llegada",blank=True, null=True)
	al100 = models.PositiveIntegerField("Días al 100%", default=0)
	al60 = models.PositiveIntegerField("Días al 60%", default=0)
	al50 = models.PositiveIntegerField("Días al 50%", default=0)
	al40 = models.PositiveIntegerField("Días al 40%", default=0)
	viaaerea = models.BooleanField("Vía Aérea",default=False)
	lineaaerea = models.ForeignKey(LineaAerea,blank=True, null=True, verbose_name="Línea Aérea")
	viaffcc = models.BooleanField("Vía FFCC",default=False)
	viabus = models.BooleanField("Vía Bus",default=False)
	lineabus = models.ForeignKey(LineaBus,blank=True, null=True, verbose_name='Empresa de Bus')
	viavehiculofiscal = models.BooleanField("Vía Vehículo Fiscal",default=False)
	vehiculofiscal = models.ForeignKey(VehiculoFiscal,blank=True, null=True, verbose_name='Vehículo Fiscal')
	viavehiculoparticular = models.BooleanField("Vía Vehículo Particular",default=False)
	placapatente = models.CharField("Placa Patente",max_length=7,blank=True,null=True)
	viataxitransfers = models.BooleanField("Via Taxi o Transfers",default=False)
	viamaritima = models.BooleanField("Via Marítima",default=False)
	kminicial = models.PositiveIntegerField("Kilometraje Incial Real", blank=True,null=True)
	kmfinal = models.PositiveIntegerField("Kilometraje Final Estimado", blank=True,null=True)
	actualizado = models.DateTimeField('Actualizado',auto_now=True, auto_now_add=False)
        creado = models.DateField('Creado',auto_now = False, auto_now_add=True)

	def __str__(self):
		return u'%s '%(self.creado)

        class Meta:
                ordering = ['-actualizado']
                verbose_name_plural = 'Cometidos'

	def get_absolute_url(self):
		return reverse("cometidos:detail", kwargs={"id": self.id})

class Destino(models.Model):
	fecha = models.DateField("Fecha", blank=False,null=False)
	establecimiento = models.ForeignKey(Establecimiento)
	objetivo = models.CharField("Objetivo", max_length=250, blank=False, null=False)
	pernoctar = models.BooleanField("Con Pernoctar",default=False)
	cometido = models.ForeignKey(Cometido)
