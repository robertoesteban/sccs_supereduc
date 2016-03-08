from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from personas.models import *
from territorios.models import *
from establecimientos.models import *
from django.utils import timezone
from django.core.urlresolvers import reverse
from django import forms
#from multiselectfield import MultiSelectField

# Create your models here.

OPCIONES_CONVOCADOPOR = (
        ('NR','Nivel Regional'),
        ('NC','Nivel Central'),
	('OT','Otro')
        )


OPCIONES_FINANCIAGASTOSDE = (
        ('AJ','Alojamiento'),
        ('AM','Alimentacion'),
	('NN','Ninguno')
        )

class Cometido(models.Model):
	rut = models.CharField("Rut",max_length=12,blank=False,null=False)
	nombre = models.CharField("Nombre Completo", max_length=180, blank=False, null=False)
	persona = models.ForeignKey(settings.AUTH_USER_MODEL, default=User)
	grado = models.CharField("Grado",max_length=60,blank=False,null=False)
	escalafon = models.CharField("Escalafon",max_length=60,blank=False,null=False)
	estamento = models.CharField("Estamento",max_length=60,blank=False,null=False)
	unidad = models.CharField("Unidad",max_length=60,blank=False,null=False)
	region = models.CharField("Region",max_length=60,blank=False,null=False)
	convocadopor = models.CharField("Convocado por", max_length=2, choices=OPCIONES_CONVOCADOPOR,blank=False,null=False)
#	financiagastosde = MultiSelectField(choices=OPCIONES_FINANCIAGASTOSDE)
	actualizado = models.DateTimeField('Actualizado',auto_now=True, auto_now_add=False)
        creado = models.DateField('Creado',auto_now = False, auto_now_add=True)
	#def __str__(self):
        #        return self.creado

	def __str__(self):
		return u'%s '%(self.creado)

        class Meta:
                ordering = ['-actualizado']
                verbose_name_plural = 'Cometidos'
	#	exclude = ('rut','nombre','grado','escalafon','estamento','unidad','region')

	def get_absolute_url(self):
		return reverse("cometidos:detail", kwargs={"id": self.id})

class Destino(models.Model):
	fecha = models.DateField("Fecha", blank=False,null=False)
	establecimiento = models.ForeignKey(Establecimiento)
	objetivo = models.CharField("Objetivo", max_length=250, blank=False, null=False)
	pernoctar = models.BooleanField("Con Pernoctar",default=False)
	cometido = models.ForeignKey(Cometido)


#	def __str__(self):
#		return self.establecimiento


