from django.contrib import admin
from cometidos.models import *
from personas.models import *
from territorios.models import *
from django.db import models
# Register your models here.
class DestinoInline(admin.TabularInline):
	model = Destino
	extra = 1

class CometidoAdmin(admin.ModelAdmin):
	list_display = ('rut','nombre')

#	fieldsets = (
#                ('Destios', {'fields': ['rut',DestinoInline], 'classes': ['collapse']})
#)


	def save_model(self, request, obj, form, change):
		if not change: 
			persona = Persona.objects.get(pk=request.user)
			obj.rut = persona.rut
			obj.grado = persona.grado
			obj.escalafon = persona.escalafon
			obj.nombre = request.user.first_name + ' ' + request.user.last_name
			obj.persona = request.user
			obj.unidad = persona.unidad
			obj.region = persona.region
			obj.save()

	def get_readonly_fields(self, request, obj=None):
		if obj: # editing an existing object
			return self.readonly_fields + ('rut', 'nombre','grado','escalafon','unidad','region')
		return self.readonly_fields

	inlines = [DestinoInline]

admin.site.register(Cometido,CometidoAdmin)
