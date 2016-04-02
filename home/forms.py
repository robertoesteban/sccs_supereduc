from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario','aria-describedby':'sizing-addon1' }))
	password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave', 'type': 'password'}))

