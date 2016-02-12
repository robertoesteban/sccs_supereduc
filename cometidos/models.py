from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Cometido(models.Model):
	desde = models.DateField(blank=False,null=False)
