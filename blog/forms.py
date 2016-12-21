from django import forms
from .models import Receta, Alimento, Ingredientes
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RecetaForm(forms.ModelForm): 

	class Meta: 
		model = Receta 
		exclude = ['fecha_publicacion']

class IngredientesForm(forms.ModelForm):

	class Meta:
		model = Ingredientes
		exclude = ['receta']

class RegistroForm(UserCreationForm):
	email = forms.EmailField(required = True)
	nombre = forms.CharField()
	apellidos = forms.CharField()
	class Meta:
		model = User
		fields = ('username', 'nombre', 'apellidos' ,'email', 'password1', 'password2')
		
	def save (self, commit = True): 
		user = super(RegistroForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['nombre']
		user.last_name = self.cleaned_data['apellidos']
		user.is_staff = False
		user.is_active = True
		user.is_superuser = False

		if commit:
			user.save()
		return user