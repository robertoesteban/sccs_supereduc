from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Region(models.Model):
	numero = models.CharField("Numero", max_length=3, blank=False, null=False)
        nombre = models.CharField("Nombre", max_length=60, blank=False, null=False)

        def __str__(self):
                return self.nombre

        class Meta:
                ordering = ['id']
                verbose_name_plural = 'Regiones'

class Comuna(models.Model):
        nombre = models.CharField("Nombre", max_length=60, blank=False, null=False)
	region = models.ForeignKey("Region",Region)
        
	def __str__(self):
                return self.nombre

        class Meta:
                ordering = ['nombre']
                verbose_name_plural = 'Comunas'

