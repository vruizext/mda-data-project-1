import psycopg2 

def connect():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5352",
                                      database="iip_db")

        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
def insertar_comision(cn,influencer_id,venta_id,producto_id,pago_id,total):
    """ Insertar una nueva comisión """
    sql = """INSERT INTO comisiones (influencer_id,venta_id,producto_id,pago_id,total) 
            VALUES (%s,%s,%s,%s,%s);"""
    vendor_id = None
    try:
        cur = cn.cursor()
        # Ejecutamos la función de INSERT
        cur.execute(sql, (influencer_id,venta_id,producto_id,pago_id,total))
        # Guardamos en la base de datos
        cn.commit()
        # Terminamos la comunicación en la base de datos
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cn is not None:
            cn.close()
cn = connect()
insertar_comision(cn,2,2,2,2,400)



