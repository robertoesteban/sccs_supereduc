from django.contrib import admin
from establecimientos.models import *
#from django_google_maps import widgets as map_widgets
#from django_google_maps import fields as map_fields

# Register your models here.

class EstablecimientoAdmin(admin.ModelAdmin):
        list_display = ('rbd', 'nombre')
#	formfield_overrides = {
#		map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
#	}

admin.site.register(Establecimiento,EstablecimientoAdmin)
admin.site.register(Sostenedor)
