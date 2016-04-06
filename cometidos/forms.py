from django import forms
from django.forms.models import inlineformset_factory
from .models import Cometido, Destino
from django.contrib.admin import widgets 


class CometidoForm(forms.ModelForm):
	class Meta:
		model = Cometido
		fields = [
			"nombre","rut","grado","estamento","escalafon","unidad","region","convocadopor","derechoaviatico","diadesalida","horadesalida","diadellegada","horadellegada","al100","al60","al50","al40","viaaerea","lineaaerea","viaffcc","viabus","lineabus","viavehiculofiscal","vehiculofiscal","viavehiculoparticular","placapatente","viataxitransfers","viamaritima","kminicial","kmfinal","tipofinanciamiento"
		]
		widgets ={
			'tipofinanciamiento': forms.CheckboxSelectMultiple,
		}

	def __init__(self, *args, **kwargs):
		super(CometidoForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance:
			self.fields['rut'].widget.attrs['readonly'] = True
			self.fields['nombre'].widget.attrs['readonly'] = True
			self.fields['grado'].widget.attrs['readonly'] = True
			self.fields['estamento'].widget.attrs['readonly'] = True
			self.fields['escalafon'].widget.attrs['readonly'] = True
			self.fields['unidad'].widget.attrs['readonly'] = True
			self.fields['region'].widget.attrs['readonly'] = True
			self.fields['convocadopor'].widget.attrs['readonly'] = True
			self.fields['diadesalida'].widget.attrs['class'] = 'form_diadesalida'
			self.fields['horadesalida'].widget.attrs['class'] = 'form_horadesalida'
			self.fields['diadellegada'].widget.attrs['class'] = 'form_diadellegada'
			self.fields['horadellegada'].widget.attrs['class'] = 'form_horadellegada'
			self.fields['nombre'].widget.attrs['size'] = 70
			self.fields['region'].widget.attrs['size'] = 70
			self.fields['rut'].widget.attrs['size'] = 14
			self.fields['grado'].widget.attrs['size'] = 6
			self.fields['estamento'].widget.attrs['size'] = 14
			self.fields['al100'].widget.attrs['size'] = 2
			self.fields['al60'].widget.attrs['size'] = 2
			self.fields['al50'].widget.attrs['size'] = 2
			self.fields['al40'].widget.attrs['size'] = 2



class DestinoForm(forms.ModelForm):
	class Meta:
		model =  Destino
		fields = [
                        "fecha","establecimiento","objetivo","pernoctar"
                ]

	def __init__(self, *args, **kwargs):
		super(DestinoForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance:
                        self.fields['fecha'].widget.attrs['class'] = 'form_fecha'
			self.fields['objetivo'].widget.attrs['size'] = 70
