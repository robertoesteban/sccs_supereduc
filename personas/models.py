from __future__ import unicode_literals

from django.db import models
from localflavor.cl.forms import CLRutField
from django.utils import timezone
# Create your models here.

OPCIONES_GENERO = (
	('H','Hombre'),
	('M','Mujer'),
	)


class Grado(models.Model):
	numero = models.PositiveIntegerField()

	def __unicode__(self):
		return str(self.numero)

	class Meta:
		ordering = ['numero']
		verbose_name_plural = 'Grados'

class Estamento(models.Model):
	nombre = models.CharField("Estamento", max_length=60, blank=False, null=False)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ['nombre']
		verbose_name_plural = 'Estamentos'


class Escalafon(models.Model):
        nombre = models.CharField("Escalafon", max_length=60, blank=False, null=False)

        def __str__(self):
                return self.nombre

        class Meta:
                ordering = ['nombre']
                verbose_name_plural = 'Escalafones'

class Unidad(models.Model):
        nombre = models.CharField("Unidad", max_length=60, blank=False, null=False)

        def __str__(self):
                return self.nombre

        class Meta:
                ordering = ['nombre']
                verbose_name_plural = 'Unidades'

class RutField(models.CharField):
        def __init__(self, *args, **kwargs):
                kwargs['max_length'] = kwargs.get('max_length',12)
                models.CharField.__init__(self, *args, **kwargs)

        def formfield(self, **kwargs):
                defaults = {'form_class': CLRutField}
                defaults.update(kwargs)
                return super(RutField, self).formfield(**defaults)



class Persona(models.Model):
        rut = RutField("Rut", unique=True, help_text='Ejemplo: 12.345.678-K')
	nombres = models.CharField("Nombres", max_length=60, blank=False, null=False)
	paterno = models.CharField("Apellido Paterno", max_length=60, blank=False, null=False)
	materno = models.CharField("Apellido Materno", max_length=60, blank=False, null=False)
	genero = models.CharField("Genero", max_length=1, choices=OPCIONES_GENERO)
	correo = models.EmailField("Correo Electronico",unique=True, blank=False, null=False)
	grado = models.ForeignKey("Grado", Grado)
	estamento = models.ForeignKey("Estamento",Estamento)
	escalafon = models.ForeignKey("Escalafon",Escalafon)
	unidad = models.ForeignKey("Unidad",Unidad)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
        timestamp = models.DateTimeField(auto_now = False, auto_now_add=True)

	def __str__(self):
		return self.nombres

	def nombre_completo(self):
		return ("%s %s %s" % (self.nombres, self.paterno,self.materno)).upper()

	class Meta:
		ordering = ['nombres']
		verbose_name_plural = 'Personas'
