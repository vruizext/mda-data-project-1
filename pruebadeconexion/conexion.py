import psycopg2

def conectarse():
    connection = psycopg2.connect(user="postgres",
                                    password="postgres",
                                    host="127.0.0.1",
                                    port="5352",
                                    database="iip_db")



def insert_comisiones (connection,comision_id,influencer_id,venta_id,producto_id,pago_id,total):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO comisiones (comision_id,influencer_id,venta_id,producto_id,pago_id,total) VALUES (%s,%s,%s,%s;%s,%s)"""
        record_to_insert = (2,2,2,2)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

def insert_composciones (connection,composicion_id,nombre,influencer_id)):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO composiones (composicion_id,nombre,influencer_id) VALUES (%s,%s,%s)"""
        record_to_insert = (2,2,2,2)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

def insert_influencers (connection,influencer_id, nombre, track_id, num_seguidores, pct_comision):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO composiones (influencer_id, nombre, track_id, num_seguidores, pct_comision) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (2,2,2,2)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

def insert_lineas_ventas (connection,venta_id, producto_id, unidades, total):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO lineas_ventas (venta_id, producto_id, unidades, total) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (2,2,2,2)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

def insert_productos (connection,venta_id, producto_id, unidades, total):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO lineas_ventas (venta_id, producto_id, unidades, total) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (2,2,2,2)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

def insert_productos_comp (connection,producto_comp_id,composicion_id,producto_id):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO lineas_ventas (producto_comp_id,composicion_id,producto_id) VALUES (%s,%s,%s)"""
        record_to_insert = (2,2,2,2)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

def insert_ventas (connection,venta_id,user_id,total,created_at):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO lineas_ventas (venta_id,user_id,total,created_at) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (2,2,2,2)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)


