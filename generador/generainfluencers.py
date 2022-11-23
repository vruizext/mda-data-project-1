from faker import Faker
from main import * 
import random

from insertar_venta import select_random
from funcion_nombre_composiciones import *

conn = connect()

def nombrecomposcion():
    faker=Faker()
    text_alt= faker.text()
    separar_text=text_alt.split()
    text_alt= (separar_text[0:3])
    nombrecom=" "
    nombrecom= nombrecom.join(text_alt)
    return nombrecom 

porcentaje=5
faker=Faker()

for i in range (5):
    nombre=faker.name()
    seguidores=random.randint(10000,1000000)
    influencer_id=insert_influencer(conn, nombre, seguidores,porcentaje)
    listaproductos=select_random(conn,2)
    comp_id=insert_composicion(conn, nombrecomposcion(), influencer_id )
    for a in listaproductos:
        print (insert_productos_comp(conn, comp_id, a[0]))

def composicionRandom (conn, limite):
    probabilidad= random.random()
    if probabilidad <= 0.03:
        sql = '''SELECT * FROM composiciones
        ORDER BY random()
        LIMIT %s'''
        cursor = conn.cursor()
        cursor.execute(sql,(limite,))
        return cursor.fetchall()[0][0]
    else:
        return 0

while True:
    
    print(composicionRandom(conn, 1))
