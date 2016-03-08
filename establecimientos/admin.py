from django.contrib import admin
from establecimientos.models import *
# Register your models here.

class EstablecimientoAdmin(admin.ModelAdmin):
        list_display = ('rbd', 'nombre')


admin.site.register(Establecimiento,EstablecimientoAdmin)
