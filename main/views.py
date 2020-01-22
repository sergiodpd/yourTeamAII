#encoding_utf-8
import os
from tkinter import messagebox

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from whoosh.fields import Schema, TEXT, BOOLEAN, NUMERIC
from whoosh.index import open_dir, create_in
from whoosh.query import Term, NumericRange, FuzzyTerm
from main.models import Jugador, Noticia
from main.forms import JugadorBusquedaForm, NoticiaBusquedaForm
from django.contrib.auth import login as do_login
import requests
from bs4 import BeautifulSoup


dirindex = "IndexWhoosh"
# Create your views here.
def index(request):
    return render(request, 'base.html')

def populate_database(request):
    populate_notices()
    populate_players()
    return HttpResponseRedirect('/')
    
def get_schema():
        return Schema(edad=NUMERIC(stored=True),
                      equipo=TEXT(stored=True),
                      goles=NUMERIC(stored=True),
                      tarjetasAmarillas=NUMERIC(stored=True),
                      tarjetasRojas=NUMERIC(Stored=True),
                      nombre=TEXT(Stored=True),
                      partidosJugados=NUMERIC(Stored=True),
                      nacionalidad=TEXT(True))
def get_news_schema():
        return Schema(titulo=TEXT(stored=True),
                      enlace=TEXT(stored=True))


def extract_notices():
    saved_notices = []
    equipos = ['barcelona','real-madrid','atletico','sevilla','getafe',
          'real-sociedad','valencia','athletic','villarreal','granada',
          'betis','levante','osasuna','alaves','valladolid',
          'eibar','mallorca','celta','leganes','espanyol']


    for e in equipos:
        url = 'https://www.marca.com/futbol/'+e +'.html?intcmp=MENUESCU&s_kw='+e
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        l =soup.find_all("h3", class_ =["mod-title"])

        
        
        for i in l:
            notice =  []
            title = i.a.get('title')
            link = i.a.get('href')  
            notice.append(title)
            notice.append(link)
            saved_notices.append(notice)    
    return saved_notices

def create_notices_index(dir_index, notice):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ind = create_in(dir_index, schema=get_news_schema())
    writer = ind.writer()

    for notic in notice:
        titulo = notic[0]
        enlace = notic[1]

        writer.add_document(titulo=str(titulo), enlace=str(enlace))

    writer.commit()


    
def populate_notices():
    notices = extract_notices()
    for notice in notices:
        title = notice[0]
        link = notice[1]
        notice = Noticia(titulo=title, enlace=link)
        print(notice)
        notice.save()
    
def extract_players():
    
    saved_players = []
    urlist = ['fc-barcelona/SKbpVP5K','real-madrid/W8mj7MDD','atletico-madrid/jaarqpLQ','sevilla/h8oAv4Ts','getafe-cf/dboeiWOt',
              'real-sociedad/jNvak2f3','valencia-cf/CQeaytrD','athletic-club/IP5zl0cJ','villarreal-cf/lUatW5jE','granada/EXuxl1xP',
              'real-betis/vJbTeCGP','levante-ud/G8FL0ShI','ca-osasuna/ETdxjU8a','alaves/hxt57t2q','real-valladolid-cf/zkpajjvm',
              'eibar/OEsEpExD','rcd-mallorca/4jDQxrbf','celta-vigo/8pvUZFhf','leganes/Mi0rXQg7','rcd-espanyol/QFfPdh1J']

    equipos = ['FC Barcelona', 'Real Madrid CdF', 'AtlÃ©tico de Madrid', 'Sevilla F.C', 'Getafe CdF', 'Real Sociedad de Futbol', 'Valencia CdF', 'Athletic Club', 'Villareal CdF', 'Granada CdF',
               'Real Betis Balompie', 'Levante UD', 'CA Osasuna', 'Deportivo AlavÃ©s', 'Real Valladolid CdF' , 'SD Eibar', 'RCD Mallorca', 'RC Celta de Vigo', 'CD LeganÃ©s', 'RCD EspanÃ±ol']

    numequipo = 0
    for u in urlist:
        url = 'https://www.mismarcadores.com/equipo/' + u + '/plantilla'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        l2 =soup.find("div", {"id": "overall-all-table"})
        l3 = l2.find_all("div", {"class": "profileTable__row profileTable__row--between profileTable__row--soccer"})
        l4 = l2.find_all("div", {"profileTable__row profileTable__row--between profileTable__row--soccer even"})
        l5 = l3 + l4
        equipo = equipos[numequipo]
        for l in l5:
            player = []
            dorsal = l.div.div.text
            nacionalidad = l.div.div.find_next_sibling("div").span.get('title')
            nombre = l.div.div.find_next_sibling("div").div.a.text
            edad = l.div.find_next_sibling("div").div.text
            partidosJugados = l.div.find_next_sibling("div").div.find_next_sibling("div").text
            goles = l.div.find_next_sibling("div").div.find_next_sibling("div").find_next_sibling("div").text
            tarjetasAmarillas = l.div.find_next_sibling("div").div.find_next_sibling("div").find_next_sibling("div").find_next_sibling("div").text
            tarjetasRojas = l.div.find_next_sibling("div").div.find_next_sibling("div").find_next_sibling("div").find_next_sibling("div").find_next_sibling("div").text
            equipojug = equipo
            player.append(edad)
            player.append(equipo)
            player.append(goles)
            player.append(tarjetasAmarillas)
            player.append(tarjetasRojas)
            player.append(nombre)
            player.append(partidosJugados)
            player.append(nacionalidad)
            saved_players.append(player)
        numequipo = numequipo + 1    
    
    return saved_players
    
def create_players_index(dir_index, players):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ind = create_in(dir_index, schema=get_news_schema())
    writer = ind.writer()

    for player in players:
        edad = player[0]
        equipo = player[1]
        goles = player[2]
        tarjetasAmarillas = player[3]
        tarjetasRojas = player[4]
        nombre = player[5]
        partidosJugados = player[6]
        nacionalidad = player[7]
        writer.add_document(edad=edad, equipo=str(equipo), goles=goles,
                            tarjetasAmarillas=tarjetasAmarillas, tarjetasRojas=tarjetasRojas,
                            nombre=str(nombre), partidosJugaods=partidosJugados, nacionalidad=str(nacionalidad))

    writer.commit()
    messagebox.showinfo("Succes",
                        "Index created correctly, " + str(len(players)) + " players saved")    
    
def populate_players():
    players = extract_players()
    for player in players:
        edad = player[0]  
        equipo = player[1]
        goles = player[2]
        tarjetasAmarillas = player[3]
        tarjetasRojas = player[4]
        nombre = player[5]
        partidosJugados = player[6]
        nacionalidad = player[7]
        
        if edad == '?':
            edad = 24
            
        if goles == '':
            goles = 0
            
        if partidosJugados == '':
            partidosJugados = 0	
            
        if tarjetasAmarillas == '':
            tarjetasAmarillas = 0
            
        if tarjetasRojas == '':
            tarjetasRojas = 0
        player = Jugador(edad=int(edad), equipos=equipo, goles=int(goles),
                            tarjetas_amarillas=int(tarjetasAmarillas), tarjetas_rojas=int(tarjetasRojas),
                            nombre=nombre, partidos_jugados=int(partidosJugados), nacionalidad=nacionalidad)
        print(player)
        player.save()
    

def ingresar(request):
    if request.user.is_authenticated:
        return (HttpResponseRedirect('/index'))
    formulario = AuthenticationForm()
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/index'))
            else:
                return (HttpResponse('<html><body>ERROR: USUARIO NO ACTIVO </body></html>'))
        else:
            return (HttpResponse('<html><body>ERROR: USUARIO O CONTARSE&Ntilde;A INCORRECTOS </body></html>'))

    return render(request, 'ingresar.html', {'formulario': formulario})

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        form.fields['username'].help_text = None
        form.fields['password1'].help_text = None
        form.fields['password2'].help_text = None
        if form.is_valid():
            user = form.save()

            if user is not None:
                do_login(request, user)

                return redirect('/')


    return render(request, "registration/register.html", {'form': form})


def busqueda_jugador(request):
    formulario = JugadorBusquedaForm()
    jugadores = []


    if request.method == 'POST':
        formulario = JugadorBusquedaForm(request.POST)
        if formulario.is_valid():
            jugadores = list(Jugador.objects.all())

            # Al inicializar todas las listas con todos los jugadores, en el caso de que alguno de los formularios no sea
            # rellenado, a la hora de la intersección será como si no afectara
            jugadores1 = Jugador.objects.all()
            jugadores2 = Jugador.objects.all()
            jugadores3 = Jugador.objects.all()
            jugadores4 = Jugador.objects.all()
            jugadores5 = Jugador.objects.all()
            jugadores6 = Jugador.objects.all()
            jugadores7 = Jugador.objects.all()
            jugadores8 = Jugador.objects.all()
            jugadores9 = Jugador.objects.all()

            nac = formulario.cleaned_data['nacionalidad']
            eq = formulario.cleaned_data['equipos']
            ed = formulario.cleaned_data['edad']
            gol = formulario.cleaned_data['goles']
            part = formulario.cleaned_data['partidos']
            amar = formulario.cleaned_data['amarillas']
            roj = formulario.cleaned_data['rojas']

            if nac != "":
                jugadores2=Jugador.objects.filter(nacionalidad=nac)
                jugadores = list(set(jugadores) & set(jugadores2))

            if eq != "":
                jugadores3 = Jugador.objects.filter(equipos__contains=eq)
                jugadores = list(set(jugadores) & set(jugadores3))

            if ed != "":
                cons = ed.split()
                # Tiene que ser de la forma "menos/más de X" o "X"
                if cons[0] == 'más':
                    jugadores4=Jugador.objects.filter(edad__gte=cons[2])

                elif cons[0] == 'menos':
                    jugadores4 = Jugador.objects.filter(edad__lte=cons[2])

                else:
                    jugadores4 = Jugador.objects.filter(edad=ed)
                jugadores = list(set(jugadores) & set(jugadores4))

            if gol != "":
                cons = gol.split()
                # Tiene que ser de la forma "menos/más de X" o "X"
                if cons[0] == 'más':
                    jugadores5=Jugador.objects.filter(goles__gte=cons[2])
                elif cons[0] == 'menos':
                    jugadores5=Jugador.objects.filter(goles__lte=cons[2])
                elif int(cons[0]) > 1:
                    jugadores5=Jugador.objects.filter(goles=gol)
                jugadores = list(set(jugadores) & set(jugadores5))

            if part != "":
                cons = part.split()
                # Tiene que ser de la forma "menos/más de X" o "X"
                if cons[0] == 'más':
                    jugadores6=Jugador.objects.filter(partidos_jugados__gte=cons[2])
                elif cons[0] == 'menos':
                    jugadores6=Jugador.objects.filter(partidos_jugados__lte=cons[2])
                elif int(cons[0]) > 1:
                    jugadores6=Jugador.objects.filter(partidos_jugados=part)
                jugadores = list(set(jugadores) & set(jugadores6))

            if amar != "":
                cons = amar.split()
                    # Tiene que ser de la forma "menos/más de X" o "X"
                if cons[0] == 'más':
                    jugadores7=Jugador.objects.filter(tarjetas_amarillas__gte=cons[2])
                elif cons[0] == 'menos':
                    jugadores7=Jugador.objects.filter(tarjetas_amarillas__lte=cons[2])
                elif int(cons[0]) > 1:
                    jugadores7=Jugador.objects.filter(tarjetas_amarillas=amar)
                jugadores = list(set(jugadores) & set(jugadores7))

            if roj != "":
                cons=roj.split()
                # Tiene que ser de la forma "menos/más de X" o "X"
                if cons[0] == 'más':
                    jugadores8=Jugador.objects.filter(tarjetas_rojas__gte=cons[2])
                elif cons[0] == 'menos':
                    jugadores8=Jugador.objects.filter(tarjetas_rojas__lte=cons[2])
                elif int(cons[0]) > 1:
                    jugadores8=Jugador.objects.filter(tarjetas_rojas=roj)
                jugadores = list(set(jugadores) & set(jugadores8))


    return render(request, 'busqueda_jugadores.html',
                  {'form': formulario, 'jugadores': jugadores})


def busqueda_noticia(request):
    form = NoticiaBusquedaForm()
    noticias = None
    if request.method == 'POST':
        form = NoticiaBusquedaForm(request.POST)
        if form.is_valid():
            noticias = Noticia.objects.all()
            keywords = form.cleaned_data['keywords']

            ix = open_dir(dirindex)
            with ix.searcher() as searcher:

                temas = keywords.split()

                for x in temas:
                    query = FuzzyTerm('titulo', x)
                    #Si no funciona bien, hacerlo con Term
                    noticias = noticias & searcher.search(query)

    else:
        form = NoticiaBusquedaForm()

    return render(request, 'busqueda_noticias.html', {'form': form, 'noticias':noticias})
