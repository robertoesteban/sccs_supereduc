from django.contrib import admin
from territorios.models import *
# Register your models here.


class ProvinciaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'region')
	list_filter = ['region']

class ComunaAdmin(admin.ModelAdmin):
        list_display = ('nombre', 'provincia','region')
        list_filter = ['provincia','region']

admin.site.register(Region)
admin.site.register(Provincia,ProvinciaAdmin)
admin.site.register(Comuna,ComunaAdmin)


