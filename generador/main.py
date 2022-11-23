from funciones import *
import random, time

# Creamos la función para hacer una query aleatoria

if __name__ == '__main__':
    conn = connect()

    # Insertar 100 influencers y composiciones si no se han insertado aún
    lista_composiciones = select_all_composiciones(conn)
    if lista_composiciones is None or len(lista_composiciones) == 0:
        lista_composiciones = generar_influencers_composiciones(conn, 100)

    while True:
        # Asignamos un usuario aleatorio
        user_id = random.randint(1, 1000000)

        # Insertamos una visita de usuario
        comp_id = composicionRandom(conn)
        insert_visita(conn, user_id,  comp_id, datetime.now(timezone.utc))

        print(f"visita user_id:{user_id} comp_id:{comp_id}")

        # Para ventas de muebles online, la conversión a ventas es en el mejor caso de un 3%
        # Los influencers tienen el poder de convertir mucho más, estimamos que en este caso será sobre un 10%
        if comp_id > 0:
            conversion_ratio = 0.1
        else:
            conversion_ratio = 0.03

        if random.random() <= conversion_ratio:
            # Marcamos el límite de los productos random
            lim = random.randint(1,10)

            # Seleccionamos productos de forma aleatoria
            productos_random = select_random(conn, lim)

            total = 0
            # Calculamos el total de la venta
            lista_productos_venta = []
            for producto in productos_random:
                unidades = random.randint(1, 4)
                precio = round(producto[4], 2)
                total += round(unidades * producto[4], 2)
                lista_productos_venta.append({ 'producto_id': producto[0], 'unidades': unidades, 'precio': precio })

            print(f"venta total:{total} comp_id:{comp_id}")

            # Recogemos el id asignado a la venta en la variable venta_id
            venta_id = insert_venta(conn, user_id, total, datetime.now(timezone.utc))

            # Inserta una linea de venta por cada producto que se ha vendido
            for producto in lista_productos_venta:
                insert_linea_venta(conn, venta_id, producto['producto_id'], producto['unidades'], producto['precio'])

            # Si la venta no ha sido generada por un influencer, no generará comisión
            if comp_id == 0:
                continue

            composicion = lista_composiciones[comp_id]
            if composicion is None:
                print(f"ERROR: composicion no se ha cargado {comp_id}")
                continue

            # Tenemos que generar comision si se ha comprado alguno de los productos de la composicion
            for producto_venta in productos_random:
                if producto_venta[0] in composicion['producto_ids']:
                    comision_eur = round(composicion['porcentaje'] * producto_venta[4], 2)
                    print(f"comision venta {venta_id}: {comision_eur}")
                    insert_comision(conn, composicion['influencer_id'], venta_id, producto_venta[0], comision_eur)

        # time.sleep(0.5)

        