from django.contrib import admin
from mediosdetransporte.models import *
from personas.models import *

# Register your models here.

class VehiculoFiscalAdmin(admin.ModelAdmin):
	list_display = ('patente', 'marca','modelo','asignado_a')


admin.site.register(LineaAerea)
admin.site.register(LineaBus)
admin.site.register(VehiculoFiscal,VehiculoFiscalAdmin)
