from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from personas.models import *
from territorios.models import *

# Create your models here.
class Cometido(models.Model):
	rut = models.CharField("Rut",max_length=12,blank=False,null=False,editable=False)
	nombre = models.CharField("Nombre Completo", max_length=180, blank=False, null=False,editable=False)
	persona = models.ForeignKey(User, default=User,editable=False)
	grado = models.CharField("Grado",max_length=60,blank=False,null=False,editable=False)
	escalafon = models.CharField("Escalafon",max_length=60,blank=False,null=False,editable=False)
	unidad = models.CharField("Unidad",max_length=60,blank=False,null=False,editable=False)
	region = models.CharField("Region",max_length=60,blank=False,null=False,editable=False)
