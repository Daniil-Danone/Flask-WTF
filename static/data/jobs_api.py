import flask
from flask import jsonify
from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print(jobs)
    if jobs:
        return jsonify(
            {
                'jobs':
                    [item.to_dict() for item in jobs]
            }
        )
    else:
        return jsonify({'error': 'Not found'})
