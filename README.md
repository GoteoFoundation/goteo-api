## API de Goteo basada en flask/sqlalchemy/flask-restful

### Instalación
En Ubuntu 14.04, primero assegurase que se tienen todas las librerias:

```bash
sudo apt-get install python-setuptools python-dev build-essential
sudo apt-get install libevent1-dev libmysqlclient-dev libpython-dev
sudo apt-get install python-virtualenv virtualenvwrapper
sudo apt-get install redis-server python-redis
sudo easy_install pip
```

Para instalar el entorno local hay 2 opciones:

1. La primera es tener los entornos centralizados en un solo sitio, para ello se usa el script mkvirtualenv:
    ```bash
    mkdir ~/.virtualenvs
    echo 'export WORKON_HOME=~/.virtualenvs' >> ~/.bashrc
    source ~/.bashrc
    mkvirtualenv goteoapi
    pip install -r requirements.txt
    ```

2. La segunda està pensada para no entrometerse con ningun script personalizado (como el .bashrc). Simplemente crea el entorno "virtual" en una subcarpeta `virtualenv` (el mismo método que usa el servidor web), para ello se puede usar el script `deployer.sh` que actualiza las dependencias automaticamente:
    ```bash
    ./deployer.sh
    ```
### Configuración

Una vez instaladas las dependencias, hay que configurar los datos de conexión a la BD:
```bash
cp config/config.py.example config/config.py
```

Editar el archivo `config.py` con los datos correctos.

### Ejecución

1. Si se ha usado el método 1, entonces solo nos queda activar el virtualenvironment y ejecutar la API:
    ```bash
    workon goteoapi
    ./goteoapi-restful.py
    ```

2. En el caso del método 2 hay que ejectutar:
    ```bash
    source virtualenv/bin/activate
    ./goteoapi-restful.py
    ```

Esto por defecto pone a la escucha un servidor web en http://0.0.0.0:5000/

## Ejemplos de uso

Lista de proyectos:

    curl -i http://0.0.0.0:5000/projects

Detalles de un proyecto concreto:

    curl -i http://0.0.0.0:5000/projects/057ce063ee014dee885b13840774463c

Listado de proyectos con un mínimo de 1000€:

    curl -i -X GET -H "Content-Type: application/json" -d '{"low_minimum":1000}' http://0.0.0.0:5000/projects/

Listado de proyectos con un mínimo de hasta 2000€:

    curl -i -X GET -H "Content-Type: application/json" -d '{"high_minimum":2000}' http://0.0.0.0:5000/projects/

Listado de proyectos con un mínimo entre 1000€ y 2000€:

    curl -i -X GET -H "Content-Type: application/json" -d '{"low_minimum":1000,"high_minimum":2000}' http://0.0.0.0:5000/projects/

Error:

    curl -i -X GET -H "Content-Type: application/json" http://0.0.0.0:5000/projects

    HTTP/1.0 400 BAD REQUEST
    Content-Type: application/json
    Content-Length: 53
    Server: Werkzeug/0.9.6 Python/2.7.6
    Date: Sun, 05 Oct 2014 10:30:41 GMT

    {
        "message": "Bad Request",
        "status": 400
    }

## Notas

Durante el desarrollo de la API sale la [versión 2.0](https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md)
de la especificación de swagger y por otra parte flask-restful-swagger solo soporta la versión 1.2.

La versión 2.0 incluye, entre otras muchas mejoras, la posibilidad de especificar parámetros múltiples desde la interfaz web
de la forma: http://URL?opt=bar&opt=foo

Más información aquí:
https://github.com/rantav/flask-restful-swagger/issues/50#issuecomment-65641980
