from flask import (Blueprint, request, jsonify)


def create_response(msg, ret_code=200):
    return jsonify(msg), ret_code


def create_error(err_msg, err_code=400):
    return jsonify(err_msg), err_code


blueprint = Blueprint("static", __name__)


@blueprint.route("/", methods=["POST"])
def register_task():
    req = request.json

    try:
        url = req["url"]
    except KeyError as e:
        return create_error("No {} in request body".format(e))

    return create_response("POST {}".format(url))


@blueprint.route("/<uuid:task_id>", methods=["GET"])
def get_results_of_task(task_id):

    return create_response("GET {}".format(task_id))


@blueprint.route("/check/<uuid:task_id>", methods=["GET"])
def check_status_of_task(task_id):

    return create_response("GET {}".format(task_id))
