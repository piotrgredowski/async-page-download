from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    send_file
)

from page_handling import Downloader


def create_response(msg, ret_code=200):
    return jsonify(msg), ret_code


def create_error(err_msg, err_code=400):
    return jsonify(err_msg), err_code


blueprint = Blueprint("jobs", __name__)


@blueprint.route("", methods=["PUT"])
def register_job():
    req_json = request.get_json()

    try:
        url = req_json["url"]
    except KeyError as e:
        return create_error("No {} in request body".format(e))
    result_ttl = current_app.cfg.get("queue.result_ttl")

    downloader = Downloader()
    job = current_app.queue.enqueue(downloader.get_page,
                                    args=(url,),
                                    result_ttl=result_ttl)

    response = {
        "job_id": job.id,
    }

    if request.args.get("debug"):
        response["next_url"] = "http://localhost:8191/api/jobs/" + job.id + "/status"

    return create_response(response)


@blueprint.route("/<uuid:job_id>/status", methods=["GET"])
def check_status_of_job(job_id):
    job = current_app.queue.fetch_job(str(job_id))

    if not job:
        return create_error("There is no job with given ID", 404)

    response = {
        "status": job.get_status(),
        "meta": job.meta,
    }

    if request.args.get("debug"):
        response["next_url"] = "http://localhost:8191/api/jobs/" + job.id

    return create_response(response)


@blueprint.route("/<uuid:job_id>", methods=["GET"])
def get_result_of_job(job_id):
    job = current_app.queue.fetch_job(str(job_id))

    if not job:
        return create_error("There is no job with given ID", 404)

    job_status = job.get_status()
    if job_status == "failed":
        return create_error("Job failed.", 409)
    elif job_status != "finished":
        return create_error("Job is not finished, try again later", 409)

    downloaded_page = job.result

    filename = downloaded_page.save_to_zip(filename=job.id)

    try:
        return send_file(filename_or_fp=filename,
                         as_attachment=True,
                         attachment_filename=job.id + ".zip")
    finally:
        downloaded_page.remove_created_files()

        if request.args.get("delete_after_download"):
            job.delete()
