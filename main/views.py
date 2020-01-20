#encoding_utf-8
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from whoosh.fields import Schema, TEXT, BOOLEAN, NUMERIC
from whoosh.index import open_dir
from whoosh.query import Term, NumericRange, FuzzyTerm
from main.models import Jugador, Noticia
from main.forms import JugadorBusquedaForm, NoticiaBusquedaForm
from django.contrib.auth import login as do_login


dirindex = "IndexWhoosh"
# Create your views here.
def index(request):
    return render(request, 'base.html')

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
    jugadores = None
    keyword1 = ''
    keyword2 = ''
    keyword3 = ''
    keyword4 = ''
    keyword5 = ''

    def get_schema():
        return Schema(edad=NUMERIC(stored=True),
                      posicion=TEXT(stored=True),
                      equipo=TEXT(stored=True),
                      goles=NUMERIC(stored=True),
                      tarjetasAmarillas=NUMERIC(stored=True),
                      tarjetasRojas=NUMERIC(Stored=True),
                      nombre=TEXT(Stored=True),
                      partidosJugados=NUMERIC(Stored=True),
                      lesionado=BOOLEAN(Stored=True),
                      nacionalidad=TEXT(True))

    if request.method == 'POST':
        formulario = JugadorBusquedaForm(request.POST)
        if formulario.is_valid():
            jugadores = Jugador.objects.all()

            #Al inicializar todas las listas con todos los jugadores, en el caso de que alguno de los formularios no sea
            #rellenado, a la hora de la intersección será como si no afectara
            jugadores1 = Jugador.objects.all()
            jugadores2 = Jugador.objects.all()
            jugadores3 = Jugador.objects.all()
            jugadores4 = Jugador.objects.all()
            jugadores5 = Jugador.objects.all()
            jugadores6 = Jugador.objects.all()
            jugadores7 = Jugador.objects.all()
            jugadores8 = Jugador.objects.all()
            jugadores9 = Jugador.objects.all()

            pos = formulario.cleaned_data['posicion']
            nac = formulario.cleaned_data['nacionalidad']
            eq = formulario.cleaned_data['equipos']
            ed = formulario.cleaned_data['edad']
            gol = formulario.cleaned_data['goles']
            part = formulario.cleaned_data['partidos']
            amar = formulario.cleaned_data['amarillas']
            roj = formulario.cleaned_data['rojas']
            les = formulario.cleaned_data['lesionado']

            ix = open_dir(dirindex)
            with ix.searcher() as searcher:
                #Para comprobar si la posición está vacía
                if pos:
                    query = Term('posicion', pos)
                    jugadores1 = searcher.search(query)
                if nac:
                    query = Term('nacionalidad', nac)
                    jugadores2 = searcher.search(query)
                if eq:
                    query = Term('equipos', eq)
                    jugadores3 = searcher.search(query)
                if ed:
                    cons = ed.split()
                    #Tiene que ser de la forma "menos/más de X" o "X"
                    if cons[0]=='más':
                        query = NumericRange('edad', int(cons[2])+1, 100)
                    elif cons[0]=='menos':
                        query = NumericRange('edad', 10, int(cons[2])-1)
                    elif int(cons[0])>1:
                        query = NumericRange('edad', int(cons[2]), int(cons[2]))
                    jugadores4 = searcher.search(query)

                if gol:
                    # Tiene que ser de la forma "menos/más de X" o "X"
                    if cons[0] == 'más':
                        query = NumericRange('goles', int(cons[2]) + 1, 2000)
                    elif cons[0] == 'menos':
                        query = NumericRange('goles', 0, int(cons[2]) - 1)
                    elif int(cons[0]) > 1:
                        query = NumericRange('goles', int(cons[2]), int(cons[2]))
                    jugadores5 = searcher.search(query)

                if part:
                    # Tiene que ser de la forma "menos/más de X" o "X"
                    if cons[0] == 'más':
                        query = NumericRange('partidosJugados', int(cons[2]) + 1, 20000)
                    elif cons[0] == 'menos':
                        query = NumericRange('partidosJugados', 0, int(cons[2]) - 1)
                    elif int(cons[0]) > 1:
                        query = NumericRange('partidosJugados', int(cons[2]), int(cons[2]))
                    jugadores6 = searcher.search(query)

                if amar:
                    # Tiene que ser de la forma "menos/más de X" o "X"
                    if cons[0] == 'más':
                        query = NumericRange('tarjetasAmarillas', int(cons[2]) + 1, 2000)
                    elif cons[0] == 'menos':
                        query = NumericRange('tarjetasAmarillas', 0, int(cons[2]) - 1)
                    elif int(cons[0]) > 1:
                        query = NumericRange('tarjetasAmarillas', int(cons[2]), int(cons[2]))
                    jugadores7 = searcher.search(query)

                if part:
                    # Tiene que ser de la forma "menos/más de X" o "X"
                    if cons[0] == 'más':
                        query = NumericRange('tarjetasRojas', int(cons[2]) + 1, 2000)
                    elif cons[0] == 'menos':
                        query = NumericRange('tarjetasRojas', 0, int(cons[2]) - 1)
                    elif int(cons[0]) > 1:
                        query = NumericRange('tarjetasRojas', int(cons[2]), int(cons[2]))
                    jugadores8 = searcher.search(query)

                if les:
                    lesion = les=='True'

                    jugadores9 = Jugador.objects.filter('lesionado'==lesion)

                jugadores = jugadores1 & jugadores2 & jugadores3 & jugadores4 & jugadores5 \
                         & jugadores6 & jugadores7 & jugadores8 & jugadores9

    return render(request, 'busqueda_jugadores.html',
                  {'form': formulario, 'jugadores': jugadores})


def busqueda_noticia(request):
    noticias = Noticia.objects.all()
    if request.method == 'POST':
        form = NoticiaBusquedaForm(request.POST)
        if form.is_valid():
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
