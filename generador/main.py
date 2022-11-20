import csv
import psycopg2
import time


def connect():
    try:
        return psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5352",
                                database="iip_db")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_influencer (conn, nombre, num_seguidores, pct_comision):
    try:
        sql = """
            INSERT INTO composiones (nombre, track_id, num_seguidores, pct_comision) 
            VALUES (%s,%s,%s,%s)
            """
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, '', num_seguidores, pct_comision))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar producto ({nombre},{num_seguidores}, {pct_comision})", error)
    finally:
        if cursor:
            cursor.close()


def insert_producto(conn, nombre, descripcion, categoria, precio):
    try:
        sql = """
            INSERT INTO productos (nombre,descripcion,categoria,precio) 
            VALUES (%s, %s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, descripcion, categoria, precio))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar producto ({nombre}, {descripcion}, {categoria}, {precio})", error)
    finally:
        if cursor:
            cursor.close()


def insert_composicion(conn, nombre, influencer_id):
    try:
        sql = """
            INSERT INTO composiciones (nombre, influencer_id) 
            VALUES (%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, influencer_id))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar composicion ({nombre}, {influencer_id})", error)
    finally:
        if cursor:
            cursor.close()


def insert_productos_comp(conn, composicion_id, producto_id):
    try:
        sql = """ 
            INSERT INTO productos_comp (composicion_id, producto_id) 
            VALUES (%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (composicion_id, producto_id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al insertar productos composicion ({composicion_id}, {producto_id})", error)
    finally:
        if cursor:
            cursor.close()


def insert_visita(conn, user_id, composicion_id, timestamp):
    try:
        sql = """
            INSERT INTO visitas (user_id, composicion_id, created_at)
            VALUES(%s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, composicion_id, timestamp))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar visita ({user_id}, {composicion_id}, {timestamp})", error)
    finally:
        if cursor:
            cursor.close()


def insert_venta(conn, user_id, total, timestamp):
    try:
        sql = """
            INSERT INTO ventas (user_id,total,created_at) 
            VALUES (%s,%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, total, timestamp))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar venta ({user_id}, {total}, {timestamp})", error)
    finally:
        if cursor:
            cursor.close()


def insert_linea_venta(conn, venta_id, producto_id, unidades, total):
    try:
        sql = """
            INSERT INTO lineas_ventas (venta_id, producto_id, unidades, total) 
            VALUES (%s,%s,%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (venta_id, producto_id, unidades, total))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar linea_venta ({venta_id}, {producto_id}, {unidades}, {total})", error)
    finally:
        if cursor:
            cursor.close()


def insert_comision(conn, influencer_id, venta_id, producto_id, total):
    try:
        sql = """
            INSERT INTO comisiones (influencer_id,venta_id,producto_id,total,pago_id) 
            VALUES (%s,%s,%s,%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (influencer_id, venta_id, producto_id, total, 0))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error al insertar comision ({influencer_id}, {venta_id}, {producto_id}, {total})", error)
    finally:
        if cursor:
            cursor.close()


def insert_productos(conn, file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            insert_producto(conn, row['name'], row['short_description'], row['category'], row['price'])


if __name__ == '__main__':
    conn = connect()
    insert_productos(conn, 'productos_ikea.csv')
    conn.close()
