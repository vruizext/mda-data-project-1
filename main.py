import psycopg2
def conn():
    try:
        print("Connecting to the PostgresSQL databese...")
        return psycopg2.connect(user="postgres",
                                    password="postgres",
                                    host="127.0.0.1",
                                    port="5352",
                                    database="iip_db")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error")

def insert_composiciones(conn, nombre, influencer_id):
    try:
        cursor = conn.cursor()
        postgres_insert_query = """ INSERT INTO composiciones (nombre, influencer_id) VALUES (%s,%s)"""
        record_to_insert = (nombre, influencer_id)
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to insert record into mobile table", error)
def insert_productos_comp(conn, composicion_id,producto_id):
    try:
        cursor = conn.cursor()
        postgres_insert_query = """ INSERT INTO productos_comp (composicion_id, producto_id) VALUES (%s,%s)"""
        record_to_insert = (composicion_id, producto_id)
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to insert record into mobile table", error)

if __name__=='__main__':
    conn=conn()

    #insert_composiciones(conn,'composicon3', 3)
    #insert_composiciones(conn,'composicon4', 4)
    insert_productos_comp(conn,3,4)
    insert_productos_comp(conn,4,5)