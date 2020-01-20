#-*- coding: utf-8 -*-
'''
Created on 14 oct. 2019

@author: ant_1
'''


import requests
from bs4 import BeautifulSoup
urlist = ['fc-barcelona/SKbpVP5K','real-madrid/W8mj7MDD','atletico-madrid/jaarqpLQ','sevilla/h8oAv4Ts','getafe-cf/dboeiWOt',
          'real-sociedad/jNvak2f3','valencia-cf/CQeaytrD','athletic-club/IP5zl0cJ','villarreal-cf/lUatW5jE','granada/EXuxl1xP',
          'real-betis/vJbTeCGP','levante-ud/G8FL0ShI','ca-osasuna/ETdxjU8a','alaves/hxt57t2q','real-valladolid-cf/zkpajjvm',
          'eibar/OEsEpExD','rcd-mallorca/4jDQxrbf','celta-vigo/8pvUZFhf','leganes/Mi0rXQg7','rcd-espanyol/QFfPdh1J']
for u in urlist:
    url = 'https://www.mismarcadores.com/equipo/' + u + '/plantilla'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    l2 =soup.find("div", {"id": "overall-all-table"})
    l3 = l2.find_all("div", {"class": "profileTable__row profileTable__row--between"})
    l4 = l2.find_all("div", {"profileTable__row profileTable__row--between even"})
    l5 = l3 + l4
    for l in l5:
        dorsal = l.div.div.text
        print('Dorsal:' + dorsal)
        nacionalidad = l.div.div.find_next_sibling("div").span.get('title')
        print ('Nacionalidad:' + nacionalidad)
        nombre = l.div.div.find_next_sibling("div").div.a.text
        print('Nombre:' + nombre)
        edad = l.div.find_next_sibling("div").div.text
        print('Edad:' + edad)
        partidosJugados = l.div.find_next_sibling("div").div.find_next_sibling("div").text
        print('Partidos Jugados:' + partidosJugados)
        golesMarcados = l.div.find_next_sibling("div").div.find_next_sibling("div").find_next_sibling("div").text
        print('Goles Marcados:' + golesMarcados)
        tarjetasAmarillas = l.div.find_next_sibling("div").div.find_next_sibling("div").find_next_sibling("div").find_next_sibling("div").text
        print('Tarjetas Amarillas:' + tarjetasAmarillas)
        tarjetasRojas = l.div.find_next_sibling("div").div.find_next_sibling("div").find_next_sibling("div").find_next_sibling("div").find_next_sibling("div").text
        print('Tarjetas Rojas:' + tarjetasRojas)
        