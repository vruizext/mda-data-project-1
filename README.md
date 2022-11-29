# Data Project 1 - Grupo 3 - EDEM MDA 2022/23

## Ikinpro (IKEA Influencer Program) 

* Iván Rodríguez
* María Sancho
* Antonio Vila
* Víctor Ruiz
* Javier Figueroa

### Iniciar el generador de datos y la base de datos:

1. `git clone git@github.com:vruizext/mda-data-project-1.git`

2. `cd mda-data-project-1`

3. `docker build -t generador:latest ./generador`

4. `docker build -t postgres_db:latest ./postgres_db`

5. `docker-compose up` 

Si no se especifican otras, se usarán las credenciales y parámetros de configuración que se especifican por
defecto en el `docker-compose.yml`. 

Para sobreescribir los valores por defecto, hay que poner los valores `NAME=VALUE`
delante del comando `docker-compose up`. Por ejemplo: 

```
POSTGRES_USER=usuario POSTGRES_PASSWORD=password docker-compose up
```

### Resetear la base de datos

Hay dos opciones: 

* Borrar el volumen `mda-data-project-1_pg_data` en la app de Docker dashboard. Al iniciar docker compose de nuevo, 
se volverá a generar la base de datos automáticamente.

* Entrar en el contenedor donde está `postgres_db` y ejecutar el script `reset_db.sh` para resetear. Este script borra 
la base de datos, genera una nueva y vuelve a recrear el esquema de datos. 

```bash
$ docker exec -it <container_id> /bin/bash
```

Y una vez ya en el contenedor,  ejecutar el script para resetear la base de datos:

```bash
$ cd usr/local/bin 
$ ./reset_db.sh 
```

### pgAdmin

Para entrar en pgAdmin, abrir un navegador y escribir: 

`localhost:5050`

Las credenciales por defecto están en el `docker-compose.yml`. 

