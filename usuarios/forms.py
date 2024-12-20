from django import forms
from django.forms import ModelChoiceField, ModelForm, widgets
from usuarios.models import Usuario
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple 




class UsuarioForm(ModelForm):
    rol= ModelChoiceField(
        queryset=Group.objects.all(),
        label="Rol",
    )
    class Meta:
        model= Usuario
        fields= "__all__"
        exclude=["estado","user"]
        widgets={
            'fecha_nacimiento':widgets.DateInput(attrs={'type':'date'},format='%Y-%m-%d')
        }

class UsuarioEditarForm(ModelForm):
    rol= ModelChoiceField(
        queryset=Group.objects.all(), 
        label="Rol",
    )
    class Meta:
        model= Usuario
        fields= "__all__"
        exclude=["estado","fecha_nacimiento", "documento","user"]
        

class GroupForm(ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=FilteredSelectMultiple('Permissions', False),
        required=False,
    )
    class Meta:
        model = Group
        fields = ['name','permissions']     