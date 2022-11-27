from funciones import *
import random
from datetime import datetime, timezone, timedelta

if __name__ == '__main__':
    conn = connect()

    if conn is None:
        print(f"Error al conectar con la base de datos: {os.getenv('POSTGRES_HOST', 'pg_server'):{os.getenv('POSTGRES_PORT', '5432')}}")
        exit(0)

    # Insertar 100 influencers y composiciones si no se han insertado aún
    lista_composiciones = select_all_composiciones(conn)
    if lista_composiciones is None or len(lista_composiciones) == 0:
        insert_productos(conn, 'productos_ikea.csv')
        lista_composiciones = generar_influencers_composiciones(conn, 100)

    # Empezamos a recoger datos de visitas 3 meses antes de nuestro experimento
    visita_ts = datetime(2022, 8, 1, tzinfo=timezone.utc)
    # En noviembre empiezan las recomendaciones de los influencers
    influencers_start_ts = datetime(2022, 11, 1, tzinfo=timezone.utc)
    # El 30 de noviembre dejamos de recoger datos
    inflencers_end_ts = datetime(2022, 11, 30, tzinfo=timezone.utc)
    # Suponemos que tenemos una visita cada 30 segundos
    delta_visitas = timedelta(seconds=30)

    while visita_ts < inflencers_end_ts:
        visita_ts += delta_visitas
        # Asignamos un usuario aleatorio
        user_id = random.randint(1, 1000000)

        # Insertamos una visita de usuario
        comp_id = composicionRandom(conn)
        insert_visita(conn, user_id,  comp_id, visita_ts)

        print(f"visita user_id:{user_id} comp_id:{comp_id} time: {visita_ts}")

        # Para ventas de muebles online, la conversión a ventas es en el mejor caso de un 3%
        # Los influencers tienen el poder de convertir mucho más, estimamos que en este caso será sobre un 10%
        if comp_id > 0:
            conversion_ratio = 0.1
        else:
            conversion_ratio = 0.03

        if random.random() > conversion_ratio:
            continue

        # El número de productos que cada cliente compra es aleatorio
        lim = random.randint(1, 10)
        # Los productos que el cliente elije también son aleatorios
        productos_random = select_random(conn, lim)

        # Los usuarios que lleguen a través de una composición comprarán algunos de los productos recomendados
        if comp_id > 0:
            composicion = lista_composiciones[comp_id]
            lista_temp = set(productos_random + list(composicion['productos'].values()))
            productos_random = set(random.sample(lista_temp, min(lim, len(lista_temp))))


        total = 0
        # Calculamos el total de la venta
        lista_productos_venta = []
        for producto in productos_random:
            unidades = random.randint(1, 3)
            precio = round(producto[4], 2)
            total += round(unidades * producto[4], 2)
            lista_productos_venta.append({ 'producto_id': producto[0], 'unidades': unidades, 'precio': precio })

        # La venta se produce entre 1 y 360 minutos después de la visita
        venta_ts = visita_ts + timedelta(minutes=random.randint(1, 360))
        print(f"venta total:{total} comp_id:{comp_id} time: {venta_ts}")

        # Recogemos el id asignado a la venta para
        venta_id = insert_venta(conn, user_id, total, venta_ts)

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
        composicion_product_ids = list(composicion['productos'].keys())
        for producto_venta in lista_productos_venta:
            if producto_venta['producto_id'] in composicion_product_ids:
                comision_eur = round( producto_venta['precio'] * producto_venta['unidades'] * composicion['porcentaje'] / 100, 2)
                print(f"comision venta {venta_id}: {comision_eur}")
                insert_comision(conn, composicion['influencer_id'], venta_id, producto_venta['producto_id'], comision_eur)

        conn.commit()
        