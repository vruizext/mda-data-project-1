import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="iip_db",
    user="postgres",
    password="postgres",
    port="5352")

def connect():
    """ Connect to the PostgreSQL database server """
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="iip_db",
            user="postgres",
            password="postgres",
            port="5352")
	
    # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

    # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# Insertar fila en tabla "productos"

def insert_productos(conn, nombre, descripcion, categoria, precio):
    try:
        cur = conn.cursor()
        sql = '''
        INSERT INTO productos (
        nombre,
        descripcion,
        categoria,
        precio
        ) VALUES (%s, %s, %s, %s)
        '''
        cur.execute(sql, (nombre, descripcion, categoria, precio))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':

    conn = psycopg2.connect(
        host="localhost",
        database="iip_db",
        user="postgres",
        password="postgres",
        port="5352")

    
    insert_productos(conn, 'Mesa_2', 'Marmol', 'Muebles', 3000)


# Insertar fila en tabla "influencers"

def insert_influencers(conn, nombre, track_id, num_seguidores, pct_comision):
    try:
        cur = conn.cursor()
        sql = '''
        INSERT INTO influencers (
        nombre,
        track_id,
        num_seguidores,
        pct_comision
        ) VALUES (%s, %s, %s, %s)
        '''
        cur.execute(sql, (nombre, track_id, num_seguidores, pct_comision))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':

    conn = psycopg2.connect(
        host="localhost",
        database="iip_db",
        user="postgres",
        password="postgres",
        port="5352")

    insert_influencers(conn, 'Ana', 2, 85000, 7500)








