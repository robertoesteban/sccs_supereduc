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
	list_display = ('creado','nombre')
#	readonly_fields = ( 'nombre','rut','grado')
	fieldsets = (
		('Informacion Personal', {'fields': [ 'nombre',( 'rut','grado','estamento','escalafon'), 'unidad'],  'classes': ['collapse']}),
		('Especificaciones', {'fields': ['convocadopor','tipofinanciamiento'], 'classes': ['collapse'] }),
	)

	
#	def get_queryset(self, request):
#		qs = super(CometidoAdmin, self).get_queryset(request)
#		if request.user.is_superuser:
#			return qs
#		return qs.filter(persona = request.user)



	def save_model(self, request, obj, form, change):
		if not change: 
			persona = Persona.objects.get(pk=request.user)
			obj.rut = persona.rut
			obj.grado = persona.grado
			obj.escalafon = persona.escalafon
			obj.estamento = persona.estamento
			obj.nombre = request.user.first_name + ' ' + request.user.last_name
			obj.persona = request.user
			obj.unidad = persona.unidad
			obj.region = persona.region
			obj.save()

#	def get_readonly_fields(self, request, obj=None):
#		if obj: # editing an existing object
#			return self.readonly_fields + ('rut', 'nombre','grado','estamento','escalafon','unidad','region','persona','convocadopor')
#		else:
#			return self.readonly_fields


	inlines = [DestinoInline]

admin.site.register(Cometido,CometidoAdmin)
admin.site.register(Financiagastosde)
admin.site.register(Tramo)
