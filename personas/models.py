from __future__ import unicode_literals

from django.db import models
from localflavor.cl.forms import CLRutField
# Create your models here.

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
	updated = models.DateTimeField("Actualizado", auto_now=True, auto_now_add=False)
        timestamp = models.DateTimeField(auto_now = False, auto_now_add=True)
	correo = models.EmailField("Correo Electronico",unique=True, blank=False, null=False)

	def __str__(self):
		return self.nombres

	def nombre_completo(self):
		return ("%s %s %s" % (self.nombres, self.paterno,self.materno)).upper()

	class Meta:
		ordering = ['nombres']
		verbose_name_plural = 'Personas'



