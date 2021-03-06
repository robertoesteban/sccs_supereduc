# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from localflavor.cl.forms import CLRutField
from django.utils import timezone
from territorios.models import Region
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.


OPCIONES_GENERO = (
	('H','Hombre'),
	('M','Mujer'),
	)


OPCIONES_PONDERACION = (
	('100','al 100%'),
	('60','al 60%'),
	('50','al 50%'),
	('40','al 40%'),
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


class Actividad(models.Model):
        nombre = models.CharField("Actividad", max_length=60, blank=False, null=False)

        def __str__(self):
                return self.nombre

        class Meta:
                ordering = ['nombre']
                verbose_name_plural = 'Actividades'


class Persona(User):
        rut = RutField("Rut", unique=True, help_text='Ejemplo: 12.345.678-K')
	nombres = models.CharField("Nombres", max_length=60, blank=False, null=False)
	paterno = models.CharField("Apellido Paterno", max_length=60, blank=False, null=False)
	materno = models.CharField("Apellido Materno", max_length=60, blank=False, null=False)
	usuario = models.CharField("Usuario",unique=True, max_length=60, blank=False, null=False)
	genero = models.CharField("Genero", max_length=1, choices=OPCIONES_GENERO)
	correo = models.EmailField("Correo Electronico",unique=True, blank=False, null=False)
	grado = models.ForeignKey("Grado", Grado)
	estamento = models.ForeignKey("Estamento",Estamento)
	escalafon = models.ForeignKey("Escalafon",Escalafon)
	unidad = models.ForeignKey("Unidad",Unidad)
	region = models.ForeignKey(Region)
	actividad = models.ForeignKey(Actividad,related_name='actividades',related_query_name='actividad')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
        timestamp = models.DateTimeField(auto_now = False, auto_now_add=True)

	def __str__(self):
		return self.nombres

	def nombre_completo(self):
		return ("%s %s %s" % (self.nombres, self.paterno,self.materno)).upper()

	class Meta:
		ordering = ['nombres']
		verbose_name_plural = 'Personas'

	def save(self):
		self.username = self.usuario
		rutlimpio = self.rut.replace('.','',2).replace('-','')
		#print rutlimpio[len(self.rut)-10:len(self.rut)-4]
		self.set_password(rutlimpio[len(self.rut)-10:len(self.rut)-4])
		self.first_name = self.nombres
		self.last_name = self.paterno + " " + self.materno
		self.email = self.correo
		self.is_staff = True
		super(Persona,self).save()
		#permission = Permission.objects.get(codename='change_cometido')
		#super(Persona,self).user_permissions.add(permission)
		#permission = Permission.objects.get(codename='add_cometido')
		#super(Persona,self).user_permissions.add(permission)
		#permission = Permission.objects.get(codename='add_destino')
		#super(Persona,self).user_permissions.add(permission)
		#permission = Permission.objects.get(codename='change_destino')
                #super(Persona,self).user_permissions.add(permission)
		#permission = Permission.objects.get(codename='delete_destino')
                #super(Persona,self).user_permissions.add(permission)




