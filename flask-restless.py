import flask.ext.restless

from model import app, db, Project

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Project, url_prefix='', collection_name='projects', exclude_columns=['category'])


@app.route('/')
def hello_world():
    return """

API de Goteo.org. <a href="/projects/">/projects/</a></br>
</br>
curl -i http://0.0.0.0:5000/projects/057ce063ee014dee885b13840774463c</br>
</br>
curl -i http://0.0.0.0:5000/projects/</br>
curl -i -X GET -H "Content-Type: application/json" -d '{"low_minimum":10000}' http://0.0.0.0:5000/projects/</br>
curl -i -X GET -H "Content-Type: application/json" -d '{"high_minimum":20000}' http://0.0.0.0:5000/projects/</br>
curl -i -X GET -H "Content-Type: application/json" -d '{"low_minimum":10000,"high_minimum":20000}' http://0.0.0.0:5000/projects/</br>
"""


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
