from flask import jsonify, request, abort
import json

from model import db, app, Project


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Project):
            return {'id': o.projectid, 'name': o.name, 'category': o.category,
                    'minimum': o.minimum, 'optimum': o.optimum}
        return json.JSONEncoder.default(self, o)


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


@app.after_request
def shutdown_session(response):
    db.session.remove()
    return response


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


@app.route('/projects/', methods=['GET'])
def list_projects():

    low_minimum = None
    high_minimum = None

    if request.json:
        low_minimum = request.json.get('low_minimum')
        high_minimum = request.json.get('high_minimum')

    projects = Project.query  # .all()
    if low_minimum:
        app.logger.debug('low')
        projects = projects.filter(Project.minimum >= low_minimum)

    if high_minimum:
        app.logger.debug('high')
        projects = projects.filter(Project.minimum <= high_minimum)

    d = []
    for p in projects:
        d.append({p.projectid: JSONEncoder().encode(p)})

    return jsonify({'projects': d})


@app.route('/projects/<string:project_id>', methods=['GET'])
def detail_project(project_id):
    p = Project.query.filter_by(projectid=project_id).first()
    if p is None:
        abort(404)
    app.logger.debug(p)
    return jsonify({project_id: JSONEncoder().encode(p)})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
