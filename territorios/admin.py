from django.contrib import admin
from territorios.models import *
# Register your models here.

class ComunaInline(admin.TabularInline):
	model = Comuna
	extra = 1


class ProvinciaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'region')
	list_filter = ['region']
	search_fields = ['nombre']

	class Meta:
		models = Provincia

	inlines = [ComunaInline]
#class ComunaAdmin(admin.ModelAdmin):
#        list_display = ('nombre', 'provincia','region')
#        list_filter = ['region','provincia']
#	search_fields = ['nombre']

#	class Meta:
#		models = Comuna




admin.site.register(Region)
admin.site.register(Provincia,ProvinciaAdmin)
#admin.site.register(Comuna,ComunaAdmin)
