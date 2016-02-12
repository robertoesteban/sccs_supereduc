from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Establecimiento(models.Model):
        rbd = models.CharField("RBD",unique=True,max_length=12,blank=False,null=False,editable=False)
