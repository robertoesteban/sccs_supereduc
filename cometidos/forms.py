from django import forms

from .models import Cometido

class CometidoForm(forms.ModelForm):
	class Meta:
		model = Cometido
		fields = [
			"nombre","rut","grado","estamento","escalafon","unidad","region","convocadopor"
		]
		#exclude = ('rut')

	def __init__(self, *args, **kwargs):
		super(CometidoForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		#self.fields.keyOrder = ['nombre','grado','rut','estamento','escalafon','unidad','region']
		if instance:
			self.fields['rut'].widget.attrs['readonly'] = True
