#encoding_utf-8
from django.forms import ModelForm
from django import forms


class JugadorBusquedaForm(forms.Form):
    posicion = forms.CharField(label="Posicion", widget=forms.TextInput)
    nacionalidad = forms.CharField(label="Nacionalidad", widget=forms.TextInput)
    equipo = forms.CharField(label="Equipo", widget=forms.TextInput)
    edad = forms.CharField(label="Edad", widget=forms.TextInput)
    goles = forms.CharField(label="Goles", widget=forms.TextInput)
    partidos = forms.CharField(label="Partidos jugados", widget=forms.TextInput)
    amarillas = forms.CharField(label="Tarjetas amarillas", widget=forms.TextInput)
    rojas = forms.CharField(label="Tarjetas rojas", widget=forms.TextInput)
    lesionado = forms.CharField(label="Lesionado", widget=forms.NullBooleanSelect)


class NoticiaBusquedaForm(forms.Form):
    keywords = forms.CharField(label="Temas de la noticia", widget=forms.TextInput)