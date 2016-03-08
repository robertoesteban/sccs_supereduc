from __future__ import unicode_literals

from django.db import models
from localflavor.cl.forms import CLRutField
from django.utils import timezone
from territorios.models import Region



OPCIONES_GENERO = (
        ('H','Hombre'),
        ('M','Mujer'),
        )



class Sostenedor(models.Model):
	rut = RutField("Rut", unique=True, help_text='Ejemplo: 12.345.678-K')
        nombres = models.CharField("Nombres", max_length=60, blank=False, null=False)
        paterno = models.CharField("Apellido Paterno", max_length=60, blank=False, null=False)
        materno = models.CharField("Apellido Materno", max_length=60, blank=False, null=False)	
	comuna = models.ForeignKey(Comuna)
        updated = models.DateTimeField(auto_now=True, auto_now_add=False)
        timestamp = models.DateTimeField(auto_now = False, auto_now_add=True)

        def __str__(self):
                return self.nombres

        def nombre_completo(self):
                return ("%s %s %s" % (self.nombres, self.paterno,self.materno)).upper()

        class Meta:
                ordering = ['nombres']
                verbose_name_plural = 'Sostenedores'

# Create your models here.
class Establecimiento(models.Model):
        rbd = models.CharField("RBD",unique=True,max_length=12,blank=False,null=False)
	nombre = models.CharField("Nombre", max_length=60, blank=False, null=False)

	def __str__(self):
                return self.nombre

        class Meta:
                ordering = ['nombre']
                verbose_name_plural = 'Establecimientos'



