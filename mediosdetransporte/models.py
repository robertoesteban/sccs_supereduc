from __future__ import unicode_literals

from django.db import models

# Create your models here.
class LineaAerea(models.Model):
	nombre = models.CharField("Linea Aerea", max_length=60, blank=False, null=False)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ['nombre']
		verbose_name_plural = 'Lineas Aereas'


class LineaBus(models.Model):
	nombre = models.CharField("Linea Bus", max_length=60, blank=False, null=False)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ['nombre']
		verbose_name_plural = 'Linea de Buses'
