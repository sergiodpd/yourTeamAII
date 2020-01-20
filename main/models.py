#encoding_utf-8
from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=25, default='', verbose_name='Nombre')
    apellidos = models.CharField(max_length=50, default='', verbose_name='Apellidos')
    usuario = models.CharField(max_length=25, default='', unique=True, verbose_name='Nombre de usuario')
    password = models.CharField(max_length=20, default='', verbose_name='Contraseña')
    idUsuario = models.IntegerField(primary_key=True)
    keywords = models.TextField()

    def __str__(self):
        return self.usuario


class Noticia(models.Model):
    titulo = models.CharField(max_length=25, default='', verbose_name='Título')
    descripcion = models.TextField(default='', verbose_name='Descripción')
    imagen = models.ImageField(verbose_name="Imagen")
    enlace = models.URLField(verbose_name='Enlace a la noticia')
    idNoticia = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.titulo


class Jugador(models.Model):
    POSICIONES = ((1, 'Delantero'), (2, 'Centrocampista'), (3, 'Defensa'), (4, 'Portero'))

    EQUIPOS = ((1, 'Deportivo Alavés'), (2, 'Athletic Bilbao'), (3, 'Atlético de Madrid'), (4, 'FC Barcelona'), (5, 'RC Celta de Vigo'),
               (6, 'SD Eibar'), (7, 'RCD Espanyol'), (8, 'Getafe CF'), (9, 'Granada CF'), (10, 'CD Leganés'),
               (11, 'Levante UD'), (12, 'RCD Mallorca'), (13, 'CA Osasuna'), (14, 'Real Betis Balompié'), (15, 'Real Madrid CF'),
               (16, 'Real Sociedad'), (17, 'Real Valladolid'), (18, 'Sevilla FC'), (19, 'Valencia CF'), (20, 'Villarreal CF'))

    nombre = models.CharField(max_length=25, default='', verbose_name='Nombre')
    posicion = models.CharField(max_length=25, default='', verbose_name='Posición', choices=POSICIONES)
    edad = models.IntegerField(verbose_name='Edad')
    goles = models.IntegerField(verbose_name='Goles')
    tarjetas_amarillas = models.IntegerField(verbose_name='Tarjetas Amarillas')
    tarjetas_rojas = models.IntegerField(verbose_name='Tarjetas rojas')
    equipos = models.CharField(max_length=25, default='', verbose_name='Equipo', choices=EQUIPOS)
    nacionalidad = models.CharField(max_length=25, default='', verbose_name='Nacionalidad')
    partidos_jugados = models.IntegerField(verbose_name='Partidos Jugados')
    idJugador = models.IntegerField(primary_key=True)
    lesionado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre