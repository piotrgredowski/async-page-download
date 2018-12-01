from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
)

from page_handling import PageDownloader


def create_response(msg, ret_code=200):
    return jsonify(msg), ret_code


def create_error(err_msg, err_code=400):
    return jsonify(err_msg), err_code


blueprint = Blueprint("jobs", __name__)


@blueprint.route("", methods=["PUT"])
def register_job():
    req = request.get_json()

    try:
        url = req["url"]
    except KeyError as e:
        return create_error("No {} in request body".format(e))
    result_ttl = current_app.cfg.get("queue.result_ttl")

    pd = PageDownloader()
    # TODO: Handle exceptions
    job = current_app.queue.enqueue(pd.get_page,
                                    args=(url,),
                                    result_ttl=result_ttl)

    return create_response({
        "job_id": job.id,
        "next_url": "http://localhost:8191/api/jobs/" + job.id + "/status"})


@blueprint.route("/<uuid:job_id>/status", methods=["GET"])
def check_status_of_job(job_id):
    job = current_app.queue.fetch_job(str(job_id))

    if not job:
        return create_error("There is no job with given ID", 404)

    return create_response({"status": job.get_status(),
                            "meta": job.meta,
                            "next_url": "http://localhost:8191/api/jobs/" + job.id})


@blueprint.route("/<uuid:job_id>", methods=["GET"])
def get_result_of_job(job_id):
    job = current_app.queue.fetch_job(str(job_id))

    if not job:
        return create_error("There is no job with given ID", 404)
    if job.get_status() != "finished":
        return create_error("Job is not finished, try again later", 409)

    downloaded_page = job.result

    # TODO: For now return only text - bytes cannot be send by json
    return create_response({"result": {"text": downloaded_page.text,
                                       "src_url": downloaded_page.url}})
