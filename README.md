# BigData

Este repositorio alberga proyectos relacionados con Big Data. A continuación, se detallan los proyectos incluidos:

## Proyectos

### 1. ContadorAgua-Vagrant

**Descripción:** Este proyecto utiliza Vagrant para configurar un entorno de desarrollo destinado al análisis de datos de consumo de agua.

**Estructura del proyecto:**

- **`Vagrantfile`:** : Archivo que contiene toda la configuración necesaria para arrancar las 2 maquinas (`servidor` y `contador`)
- **`Contador.py/`:** : Simulador de una contador de agua, emitiendo 60 pulsos (segundos) por cada vez iniciado por el cron
- **`Servidor.py/`:** : API REST con Flask, que gestiona la recepción de los datos enviados por el `contador` y los guarda en su base de datos postgres

**Cómo iniciar el entorno:**

1. : Ejecutamos el `vagrantfile` mediante el comando `vagrant up`
2. : Esperamos a que el cron inicie el `contador.py`
3. : Mediante el endpoint `http://192.168.33.10:5000/cosumoGlobal` ya podremos consultar los datos insertados en la base de datos

