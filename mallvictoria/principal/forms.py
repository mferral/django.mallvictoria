#encoding:utf-8
from django.forms import ModelForm, Textarea, TextInput
from django import forms
from principal.models import Articulo, Usuario, Ciudad

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        widgets={
        	'descripcion':Textarea(attrs={'cols':30,'rows':3}),
        	'titulo':TextInput(attrs={'placeholder':'Nombre del Articulo (maximo 30 caracteres)'}),
        }
    def __init__(self, *args, **kwargs):
    	super(ArticuloForm, self).__init__(*args, **kwargs)
    	self.fields['categoria'].empty_label = None
    	self.fields['tipo'].empty_label = None

class ArticuloFormEdit(forms.ModelForm):
    class Meta:
        model = Articulo
        widgets={
            'descripcion':Textarea(attrs={'cols':30,'rows':3}),
            'titulo':TextInput(attrs={'placeholder':'Nombre del Articulo (maximo 30 caracteres)'}),
        }
        fields=['titulo','descripcion','tipo','categoria','costo']
    def __init__(self, *args, **kwargs):
        super(ArticuloFormEdit, self).__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = None
        self.fields['tipo'].empty_label = None

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
    def __init__(self, *args, **kwargs):
        super(UsuarioForm,self).__init__(*args, **kwargs)
        self.fields['ciudad'].queryset=Ciudad.objects.filter(estado=self.instance.estado)
    