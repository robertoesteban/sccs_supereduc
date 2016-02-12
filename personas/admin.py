from django.contrib import admin
from personas.models import *
# Register your models here.

class PersonaAdmin(admin.ModelAdmin):
	list_display = ('rut', 'nombre_completo','unidad','usuario')
	fieldsets = (
		('Informacion Personal', {'fields': ('rut', 'nombres',( 'paterno', 'materno'), 'correo', ('usuario', 'genero'))}),
		('Datos de Contratacion', {'fields': [('grado','escalafon', 'estamento'), 'unidad','region'], 'classes': ['collapse']})
)

admin.site.register(Grado)
admin.site.register(Persona,PersonaAdmin)
admin.site.register(Estamento)
admin.site.register(Escalafon)
admin.site.register(Unidad)
