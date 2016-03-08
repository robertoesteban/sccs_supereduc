from django import forms

from .models import Cometido

class CometidoForm(forms.ModelForm):
	class Meta:
		model = Cometido
		fields = [
			"rut","nombre","grado","estamento","escalafon","unidad","region","convocadopor"
		]
		#exclude = ('rut')
