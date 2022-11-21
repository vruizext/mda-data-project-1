from main import *
import random



def select_random(conn,lim):

    sql = '''SELECT * FROM productos
    ORDER BY random()
    LIMIT %s'''
    cursor = conn.cursor()
    cursor.execute(sql,(lim,))
    return cursor.fetchall()
        
if __name__ == '__main__':
    conn = connect()
    lim = random.randint(1,10)
    productos_random = select_random(conn,lim)
    
    #1. Crear venta necesitamos total
    
    total = 0

    for r in productos_random:
       print (r)
       total += round(r[4],2)
    
    print (total)
    user_id = random.randint(1000,10000)
    venta_id = insert_venta(conn, user_id, total, datetime.now(timezone.utc))
    unidades = 1
    for r in productos_random:
        insert_linea_venta(conn, venta_id, r[0],unidades,round(r[4],2))

    #3. User id

    


    #insert_venta(conn, user_id, total, datetime.now(timezone.utc))




