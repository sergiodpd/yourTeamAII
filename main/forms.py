#encoding_utf-8
from django.forms import ModelForm
from django import forms


class JugadorBusquedaForm(forms.Form):
    nacionalidad = forms.CharField(label="Nacionalidad", widget=forms.TextInput, required=False)
    equipos = forms.CharField(label="Equipo", widget=forms.TextInput, required=False)
    edad = forms.CharField(label="Edad", widget=forms.TextInput, required=False)
    goles = forms.CharField(label="Goles", widget=forms.TextInput, required=False)
    partidos = forms.CharField(label="Partidos jugados", widget=forms.TextInput, required=False)
    amarillas = forms.CharField(label="Tarjetas amarillas", widget=forms.TextInput, required=False)
    rojas = forms.CharField(label="Tarjetas rojas", widget=forms.TextInput, required=False)


class NoticiaBusquedaForm(forms.Form):
    keywords = forms.CharField(label="Temas de la noticia", widget=forms.TextInput)