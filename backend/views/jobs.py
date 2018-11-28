from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    send_file,
)

from jobs_queue import q
from jobs_queue import tasks


def create_response(msg, ret_code=200):
    return jsonify(msg), ret_code


def create_error(err_msg, err_code=400):
    return jsonify(err_msg), err_code


blueprint = Blueprint("jobs", __name__)


@blueprint.route("", methods=["PUT"])
def register_job():
    req = request.json

    try:
        url = req["url"]
    except KeyError as e:
        return create_error("No {} in request body".format(e))

    result_ttl = current_app.cfg.get("queue.result_ttl")

    # TODO: Handle exceptions
    job = q.enqueue(tasks.get_page, args=(url,), result_ttl=result_ttl)

    return create_response({"next_url": "http://localhost:8191/api/jobs/" + job.id + "/status"})


@blueprint.route("/<uuid:job_id>/status", methods=["GET"])
def check_status_of_job(job_id):
    job = q.fetch_job(str(job_id))

    if not job:
        return create_error("There is no job with given ID", 404)

    return create_response({"status": job.status,
                            "next_url": "http://localhost:8191/api/jobs/" + job.id})


@blueprint.route("/<uuid:job_id>", methods=["GET"])
def get_result_of_job(job_id):
    job = q.fetch_job(str(job_id))

    if not job:
        return create_error("There is no job with given ID", 404)

    return create_response({"result": job.result})
