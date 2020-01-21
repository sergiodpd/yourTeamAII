from bs4 import BeautifulSoup
import requests
from _overlapped import NULL

equipos = ['barcelona','real-madrid','atletico','sevilla','getafe',
          'real-sociedad','valencia','athletic','villarreal','granada',
          'betis','levante','osasuna','alaves','valladolid',
          'eibar','mallorca','celta','leganes','espanyol']


for e in equipos:
    url = 'https://www.marca.com/futbol/'+e +'.html?intcmp=MENUESCU&s_kw='+e
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    l =soup.find_all("h3", class_ =["mod-title"])
    
    notices = list()
    enlaces = list()

    
    
    for i in l:
        
        notices.append(i.a.get('title'))
        enlaces.append(i.a.get('href'))
    print('Noticias del ' + e)
    print (notices)
    print (enlaces)
    
    
     
       

