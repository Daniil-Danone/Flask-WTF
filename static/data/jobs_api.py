import flask
import sqlalchemy_serializer
from flask import jsonify, request
from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_all_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    if jobs:
        return jsonify(
            {
                'jobs':
                    [item.to_dict() for item in jobs]
            }
        )
    else:
        return jsonify({'error': 'Not found'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_news(job_id):
    try:
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).get(job_id)
        if jobs:
            return jsonify(
                {
                    'jobs':
                        [jobs.to_dict()]
                }
            )
        else:
            return jsonify({'error': 'Not found'})
    except:
        return jsonify({'error': 'Not found'})


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs()
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})
