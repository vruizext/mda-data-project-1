import csv
import psycopg2
import time


def connect():
    """Conecta con PostgresDB"""
    try:
        return psycopg2.connect(user="postgres",
                                password="postgres",
                                host="localhost",
                                port="5352",
                                database="iip_db")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_visita(conn, user_id, composicion_id, timestamp):
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO
            visitas (user_id, composicion_id, created_at)
            VALUES(%s, %s, %s)
        """

        cursor.execute(sql, (user_id, composicion_id, timestamp))

    except (Exception, psycopg2.Error) as error:
        print("Error al insertar visita", error)
    finally:
        if conn:
            conn.commit()
            cursor.close()


def insert_producto(conn, nombre, descripcion, categoria, precio):
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO 
            productos (nombre,descripcion,categoria,precio) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, categoria, precio))
    except (Exception, psycopg2.Error) as error:
        print("Error al insertar producto", error)
    finally:
        if conn:
            cursor.close()


def insert_productos(conn, file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            insert_producto(conn, row['name'], row['short_description'], row['category'], row['price'])
    conn.commit()


if __name__ == '__main__':
    conn = connect()
    insert_productos(conn, 'productos_ikea.csv')
    conn.close()
