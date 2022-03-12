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


@blueprint.route('/api/jobs/<string:job_id>', methods=['GET'])
def get_news(job_id):
    if str(job_id).isdigit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(int(job_id))
        if job:
            return jsonify(
                {
                    'jobs':
                        [job.to_dict()]
                }
            )
        else:
            return jsonify({'error': 'Not found'})
    else:
        return jsonify({'error': 'Not found'})


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job_title', 'job_describe', 'team_leader', 'work_size', 'collaborators', 'start_date', 'creator', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(int(request.json['id']))
    if not job:
        try:
            job = Jobs(
                id=request.json['id'],
                job_title=request.json['job_title'],
                job_describe=request.json['job_describe'],
                team_leader=request.json['team_leader'],
                work_size=request.json['work_size'],
                collaborators=request.json['collaborators'],
                start_date=request.json['start_date'],
                creator=request.json['creator'],
                is_finished=request.json['is_finished']
            )
            db_sess.add(job)
            db_sess.commit()
            return jsonify({'success': 'OK'})
        except Exception as ex:
            return jsonify({'error': ex})

    else:
        return jsonify({'error': 'id already exist'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})
