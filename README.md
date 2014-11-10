## API de Goteo basada en flask/sqlalchemy/flask-restful

### Instalación
En Ubuntu:

    sudo apt-get install libevent1-dev virtualenvwrapper libmysqlclient-dev libpython-dev
    mkdir ~/.virtualenvs
    echo 'export WORKON_HOME=~/.virtualenvs' >> ~/.bashrc
    source ~/.bashrc
    mkvirtualenv goteoapi
    pip install -r requirements.txt

Una vez instaladas las dependencias solo hay que activar el virtualenvironment y ejecutar la API:

    workon goteoapi
    ./flask-restful.py

Esto por defecto pone a la escucha un servidor web en http://0.0.0.0:5000/

Para usar la API:

    curl -i http://0.0.0.0:5000/projects
    curl -i http://0.0.0.0:5000/projects/057ce063ee014dee885b13840774463c
    curl -i -X GET -H "Content-Type: application/json" -d '{"low_minimum":1000}' http://0.0.0.0:5000/projects/
    curl -i -X GET -H "Content-Type: application/json" -d '{"high_minimum":2000}' http://0.0.0.0:5000/projects/
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
