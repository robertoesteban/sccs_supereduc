# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from personas.models import Persona
from django.db import models

# Create your models here.
class LineaAerea(models.Model):
	nombre = models.CharField("Linea Aerea", max_length=60, blank=False, null=False)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ['nombre']
		verbose_name = 'Linea Aerea'
		verbose_name_plural = 'Lineas Aereas'


class LineaBus(models.Model):
	nombre = models.CharField("Linea Bus", max_length=60, blank=False, null=False)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ['nombre']
		verbose_name_plural = 'Linea de Buses'

class VehiculoFiscal(models.Model):
	patente = models.CharField("Patente", unique=True, max_length=7, blank=False, null=False)
	marca = models.CharField("Marca",  max_length=60, blank=False, null=False)
	modelo = models.CharField("Modelo",  max_length=60, blank=False, null=False)
	agno = models.CharField("Año", max_length=4, blank=False, null=False)
	persona = models.ForeignKey(Persona,verbose_name='persona', limit_choices_to={'actividad': 2})

	def __str__(self):
		return self.patente

	class Meta:
		ordering = ['patente']
		verbose_name_plural = 'Vehiculos Fiscales'
	
	def asignado_a(self):
		return ("%s %s %s" % (self.persona.nombres, self.persona.paterno, self.persona.materno)).upper()



