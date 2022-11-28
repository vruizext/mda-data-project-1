import csv
import os
import random
import psycopg2
from faker import Faker


def connect():
    try:
        return psycopg2.connect(user=f"{os.getenv('POSTGRES_USER', 'postgres')}",
                                password=f"{os.getenv('POSTGRES_PASSWORD', 'postgres')}",
                                host=f"{os.getenv('POSTGRES_HOST', 'localhost')}",
                                port=f"{os.getenv('POSTGRES_PORT', '5432')}",
                                database=f"{os.getenv('POSTGRES_DB', 'iip_db')}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_influencer (conn, nombre, num_seguidores, pct_comision):
    try:
        sql = """
            INSERT INTO influencers (nombre, num_seguidores, pct_comision) 
            VALUES (%s,%s,%s) 
            RETURNING influencer_id
            """
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, num_seguidores, pct_comision))
        # conn.commit()
        return cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar producto ({nombre},{num_seguidores}, {pct_comision})", error)


def insert_producto(conn, nombre, descripcion, categoria, precio):
    try:
        sql = """
            INSERT INTO productos (nombre,descripcion,categoria,precio) 
            VALUES (%s, %s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, descripcion, categoria, precio))
        # conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar producto ({nombre}, {descripcion}, {categoria}, {precio})", error)


def insert_composicion(conn, nombre, influencer_id):
    try:
        sql = """
            INSERT INTO composiciones (nombre, influencer_id) 
            VALUES (%s,%s)
            RETURNING composicion_id
        """
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, influencer_id))
        # conn.commit()
        return cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar composicion ({nombre}, {influencer_id})", error)


def insert_productos_comp(conn, composicion_id, producto_id):
    try:
        sql = """ 
            INSERT INTO productos_comp (composicion_id, producto_id) 
            VALUES (%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (composicion_id, producto_id))
        # conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al insertar productos composicion ({composicion_id}, {producto_id})", error)


def insert_visita(conn, user_id, composicion_id, timestamp):
    try:
        sql = """
            INSERT INTO visitas (user_id, composicion_id, created_at)
            VALUES(%s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, composicion_id, timestamp))
        # conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar visita ({user_id}, {composicion_id}, {timestamp})", error)


def insert_venta(conn, user_id, total, timestamp):
    try:
        sql = """
            INSERT INTO ventas (user_id,total,created_at) 
            VALUES (%s,%s,%s)
            RETURNING venta_id
        """
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, total, timestamp))
        # conn.commit()
        return cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar venta ({user_id}, {total}, {timestamp})", error)


def insert_linea_venta(conn, venta_id, producto_id, unidades, total):
    try:
        sql = """
            INSERT INTO lineas_ventas (venta_id, producto_id, unidades, total) 
            VALUES (%s,%s,%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (venta_id, producto_id, unidades, total))
        # conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar linea_venta ({venta_id}, {producto_id}, {unidades}, {total})", error)


def insert_comision(conn, influencer_id, venta_id, producto_id, total):
    try:
        sql = """
            INSERT INTO comisiones (influencer_id,venta_id,producto_id,total) 
            VALUES (%s,%s,%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (influencer_id, venta_id, producto_id, total))
        # conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar comision ({influencer_id}, {venta_id}, {producto_id}, {total})", error)


def insert_productos(conn, file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            insert_producto(conn, row['name'], row['short_description'].strip(), row['category'], row['price'])
    conn.commit()

def select_productos_composicion(conn, comp_id):
    sql = '''
    SELECT * FROM composiciones
    WHERE composicion_id = %s
    '''
    cursor = conn.cursor()
    cursor.execute(sql, [comp_id])
    return cursor.fetchall()


def select_productos_random(conn, lim):
    """
    Selectiona productos de forma aleatoria, dando más peso a los productos más baratos
    :param conn:
    :param lim:
    :return:
    """

    sql = '''
    SELECT * FROM productos
    ORDER BY (random() * log(precio / 2))  
    LIMIT %s
    '''
    cursor = conn.cursor()
    cursor.execute(sql,(lim,))
    return cursor.fetchall()


def nombrecomposcion():
    faker=Faker()
    text_alt= faker.text()
    separar_text=text_alt.split()
    text_alt= (separar_text[0:3])
    nombrecom=" "
    nombrecom= nombrecom.join(text_alt)
    return nombrecom


def generar_influencers_composiciones(conn, limit=10):
    faker = Faker()
    porcentaje = 5
    composiciones = {}
    for i in range(limit):
        nombre = faker.name()
        seguidores = random.randint(10000, 1000000)
        influencer_id = insert_influencer(conn, nombre, seguidores, porcentaje)
        comp_id = insert_composicion(conn, nombrecomposcion(), influencer_id)
        composicion = {'comp_id': comp_id, 'porcentaje': porcentaje, 'influencer_id': influencer_id, 'productos': {}}
        listaproductos = select_productos_random(conn, random.randint(5, 10))
        for producto in listaproductos:
            insert_productos_comp(conn, comp_id, producto[0])
            composicion['productos'][producto[0]] = producto

        composiciones[comp_id] = composicion

    conn.commit()
    return composiciones


def select_composicion_random(conn):
    """
    Selecciona una composicioón de forma aleatoria, dando más peso a las composiciones
    de influencers que tienen más seguidores.
    :param conn:
    :param limite:
    :return:
    """
    try:
        sql = '''SELECT composicion_id 
                 FROM composiciones
                 INNER JOIN influencers on influencers.influencer_id = composiciones.influencer_id
                 ORDER BY (random() * log(num_seguidores)) DESC
                 LIMIT 1'''
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()[0][0]
    except (Exception, psycopg2.Error) as error:
        print(f"Error al seleccionar composiciones ", error)


def composicionRandom (conn):
    probabilidad= random.random()
    if probabilidad <= 0.03:
        return select_composicion_random(conn)
    else:
        return 0


def select_all_composiciones(conn):
    try:
        sql = '''
            SELECT 
            composiciones.composicion_id, 
            influencers.influencer_id,
            influencers.pct_comision 
            FROM composiciones
            INNER JOIN influencers on composiciones.influencer_id = influencers.influencer_id
            ORDER BY composicion_id
        '''

        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        rows = cursor.fetchall()
        composiciones = {}

        if len(rows) == 0:
            return composiciones

        for comp in rows:
            composicion = { 'comp_id': comp[0], 'influencer_id': comp[1], 'porcentaje': comp[2], 'productos': {} }
            productos_comp = select_productos_comp(conn, comp[0])
            for producto  in productos_comp:
                composicion['productos'][producto[0]] = producto
            composiciones[comp[0]] = composicion

        return composiciones
    except (Exception, psycopg2.Error) as error:
        print(f"Error al seleccionar productos_com", error)


def select_productos_comp(conn, comp_id):
    try:
        sql = '''
            SELECT productos.* 
            FROM productos
            INNER JOIN productos_comp on productos_comp.producto_id = productos.producto_id
            WHERE productos_comp.composicion_id = %s
        '''
        cursor = conn.cursor()
        cursor.execute(sql, [comp_id])
        # conn.commit()
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al seleccionar productos_com ({comp_id})", error)

