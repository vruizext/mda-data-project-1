from funciones import *
import random
from datetime import datetime, timezone, timedelta
from time import sleep

if __name__ == '__main__':
    # Esperamos hasta que la base de datos esté lista
    db_ready = False
    while not db_ready:
        sleep(5)
        db_ready = wait_for_db()

    # Inicializar random para que genere las mismas secuencias siempre
    random.seed(1)

    conn = connect()

    if conn is None:
        print(f"Error al conectar con la base de datos: {os.getenv('POSTGRES_HOST', 'pg_server'):{os.getenv('POSTGRES_PORT', '5432')}}")
        exit(0)

    # Insertar 100 influencers y composiciones si no se han insertado aún
    # Guardamos la referencia a las composiciones y los productos para usarlas
    # en el cálculo de comisiones
    lista_composiciones = select_all_composiciones(conn)
    if lista_composiciones is None or len(lista_composiciones) == 0:
        insert_productos(conn, 'productos_ikea.csv')
        lista_composiciones = generar_influencers_composiciones(conn, 100)

    # En noviembre empiezan las recomendaciones de los influencers
    visita_ts = datetime(2021, 11, 1, tzinfo=timezone.utc)
    # El 30 de noviembre dejamos de recoger datos
    end_ts = datetime(2022, 11, 30, tzinfo=timezone.utc)
    # Suponemos que tenemos una visita cada 1 segundo, 86.4k por día
    delta_visitas = timedelta(seconds=15)

    while visita_ts < end_ts:
        visita_ts += delta_visitas
        # Llega una nueva visita
        # Asumimos que las recomendaciones de los influencers suponen el 3% del tráfico
        if random.random() <= 0.03:
            # Al 3% de visitas que vienen recomendadas por influencers, les asignamos una
            # composición de forma aleatoria
            comp_id = select_composicion_random(conn)
        else:
            # El resto viene sin recomendación, su visita no se asocia a una composición
            comp_id = 0

        user_id = random.randint(1, 1000000)
        insert_visita(conn, user_id,  comp_id, visita_ts)
        print(f"visita user_id:{user_id} comp_id:{comp_id} time: {visita_ts}")

        # Para IKEA se estima que la conversión de ventas online es un 2.2% aprox.
        # http://guesswork-live.appspot.com/research/fr/ecommerce/companies/ikea.com
        # Los influencers tienen el poder de convertir mucho más. Para nuestro experiemento asumimos el doble, un 4.4%
        if comp_id > 0:
            conversion_ratio = 0.044
            # El número de productos que cada cliente compra es aleatorio, pero también estimamos que los usuarios
            # que vienen recomendados por influencers comprarán más, en media, si deciden comprar toda la composición.
            lim_productos = random.randint(1, len(lista_composiciones[comp_id]['productos']))
        else:
            conversion_ratio = 0.022
            # Para clientes que no vienen recomendados, limitamos a 4 productos, porque la compra media
            # en IKEA online es de unos 100 eur.
            lim_productos = random.randint(1, 4)

        # Simulamos la conversión a compra con una distribución aleatoria
        if random.random() > conversion_ratio:
            continue

        # Los productos que el cliente elije también son aleatorios
        productos_random = select_productos_random(conn, lim_productos)

        # Los usuarios que lleguen a través de una composición comprarán algunos de los productos recomendados
        if comp_id > 0:
            composicion = lista_composiciones[comp_id]
            lista_temp = set(productos_random + list(composicion['productos'].values()))
            productos_random = set(random.sample(lista_temp, min(lim_productos, len(lista_temp))))

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
            insert_linea_venta(conn, venta_id, producto['producto_id'], producto['unidades'], producto['unidades'] * producto['precio'])

        # Si la venta no ha sido generada por un influencer, no generará comisión
        if comp_id == 0:
            continue

        if comp_id not in lista_composiciones.keys():
            print(f"ERROR: composición no se ha cargado correctamente: {comp_id}")
            continue

        composicion = lista_composiciones[comp_id]

        # Tenemos que generar comision si se ha comprado alguno de los productos de la composicion
        composicion_product_ids = list(composicion['productos'].keys())
        for producto_venta in lista_productos_venta:
            if producto_venta['producto_id'] in composicion_product_ids:
                comision_eur = round(producto_venta['precio'] * producto_venta['unidades'] * composicion['porcentaje'] / 100, 2)
                print(f"comision venta {venta_id}: {comision_eur}")
                insert_comision(conn, composicion['influencer_id'], venta_id, producto_venta['producto_id'], comision_eur)

        conn.commit()
        