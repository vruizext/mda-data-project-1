from main import *
import random,time


# Creamos la función para hacer una query aleatoria

def select_random(conn,lim):

    sql = '''SELECT * FROM productos
    ORDER BY random()
    LIMIT %s'''
    cursor = conn.cursor()
    cursor.execute(sql,(lim,))
    return cursor.fetchall()
        
if __name__ == '__main__':
    
    while True:

        conn = connect()
        
        # Asignamos un usuario aleatorio

        user_id = random.randint(1000,10000)

        # Insertamos una visita de usuario

        insert_visita(conn, user_id, 0 , datetime.now(timezone.utc))

        print(user_id)

        # Aproximadamente el 5% de las visitas se transforman en ventas

        if random.random() >= 0.95:
            
            # Marcamos el límite de los productos random

            lim = random.randint(1,10)

            # Seleccionamos productos de forma aleatoria

            productos_random = select_random(conn,lim)

            # Hace la suma de los precios de todos los productos seleccionados

            total = 0

            for producto in productos_random:
                total += round(producto[4],2)

            # Recogemos el id asignado a la venta en la variable venta_id

            venta_id = insert_venta(conn, user_id, total, datetime.now(timezone.utc))
            
            # Inserta tantas lineas de venta como productos que corresponden a una venta

            unidades = 1
            
            for producto in productos_random:
                insert_linea_venta(conn, venta_id, producto[0],unidades,round(producto[4],2))
            
            print(venta_id)
        
        time.sleep(0.5)

        