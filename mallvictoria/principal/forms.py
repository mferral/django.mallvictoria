#encoding:utf-8
from django.forms import ModelForm, Textarea, TextInput, ModelChoiceField
from django import forms
from principal.models import Articulo, Usuario, Ciudad

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        widgets={
        	'descripcion':Textarea(attrs={'cols':30,'rows':3}),
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
        }
        fields=['titulo','descripcion','tipo','categoria','costo']
    def __init__(self, *args, **kwargs):
        super(ArticuloFormEdit, self).__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = None
        self.fields['tipo'].empty_label = None

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields=['nombre','telefono','direccion','sitioweb','estado']
    def __init__(self, *args, **kwargs):
        super(UsuarioForm,self).__init__(*args, **kwargs)
        self.fields['estado'].empty_label = None       
        #self.fields['ciudad']=forms.ModelChoiceField(queryset=Ciudad.objects.filter(estado=self.instance.estado))