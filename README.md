## API de Goteo basada en flask/sqlalchemy/flask-restful

### Instalación
En Ubuntu:

    sudo apt-get install python-setuptools python-dev build-essential
    sudo apt-get install libevent1-dev libmysqlclient-dev libpython-dev
    sudo apt-get install python-virtualenv virtualenvwrapper
    sudo easy_install pip
    mkdir ~/.virtualenvs
    echo 'export WORKON_HOME=~/.virtualenvs' >> ~/.bashrc
    source ~/.bashrc
    mkvirtualenv goteoapi
    pip install -r requirements.txt

### Configuración

Una vez instaladas las dependencias, hay que configurar los datos de conexión a la BD:
    cp config/config.py.example config/config.py

Editar el archivo config.py con los datos correctos.

### Ejecución

Solo nos queda activar el virtualenvironment y ejecutar la API:

    workon goteoapi
    ./flask-restful.py

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
