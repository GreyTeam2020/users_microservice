import connexion
from database import init_db
import logging
from flask import request, jsonify, current_app
from services.user_service import UserService


db_session = None


def _get_response(message: str, code: int):
    """
    This method contains the code to make a new response for flask view
    :param message: Message response
    :param code: Code result
    :return: a json object that look like {"result": "OK"}
    """
    return {"result": message}, code


def create_user():
    """
    This flask method give the possibility to create a new customer
    with a json request
    :return: the correct response that looks like {"result": "OK"}, 200
    :return:
    """
    if request.method == "POST":
        json = request.get_json()
        email = json["email"]
        phone = json["phone"]
        user = UserService.user_is_present(db_session, email, phone)
        if user is not None:
            return _get_response(
                "User with email {} and/or phone already exist".format(email, phone),
                500,
            )
        user = UserService.create_user(db_session, json)
        if user is not None:
            return _get_response("OK", 200)
        else:
            return _get_response(
                "User not created because we have an error on server", 500
            )
    return _get_response("Resource not found", 400)


def create_operator():
    """
    This flask method give the possibility to create a new operator
    with a json request
    :return: the correct response that looks like {"result": "OK"}, 200
    """
    if request.method == "POST":
        json = request.get_json()
        email = json["email"]
        phone = json["phone"]
        user = UserService.user_is_present(db_session, email, phone)
        if user is not None:
            return _get_response(
                "User with email {} and/or phone already exist".format(email, phone),
                500,
            )
        user = UserService.create_user(db_session, json, 3)
        if user is not None:
            return _get_response("OK", 200)
        else:
            return _get_response(
                "User not created because we have an error on server", 500
            )
    return _get_response("Resource not found", 400)


def modify_user(id):
    """
    This API method contains the logic to modify a new user
    :return: the correct response that looks like {"result": "OK"}, 200
    """
    json = request.get_json()
    current_app.logger.debug("Modify user with id {}".format(id))
    current_app.logger.debug("Request content \n{}".format(json))
    if request.method == "PUT":
        user = UserService.modify_user(db_session, json, id)
        current_app.logger.debug(
            "User after modify operation \n{}".format(user.serialize())
        )
        return _get_response(user.serialize(), 200)
    return _get_response("Resource not found", 400)


def delete_user(id):
    """
    This API method contains the logic to delete a user on database
    :return: the correct response that looks like {"result": "OK"}, 200
    """
    if request.method == "DELETE":
        user = UserService.user_is_present_with_id(db_session, id)
        if user is None:
            current_app.logger.warn(
                "The user with id {} doesn't exist, I can not delete it".format(id)
            )
            return _get_response("User not exist", 500)
        if UserService.delete_user(db_session, id):
            return _get_response("OK", 200)
        else:
            return _get_response("User unauthenticated", 500)
    return _get_response("Resource not found", 400)


def login_user():
    """
    This API method contains the logic authenticate the user
    :return: the correct response contains the user with id role
    """
    if request.method == "POST":
        json = request.get_json()
        user = UserService.user_login(
            db_session, email=json["email"], password=json["password"]
        )
        if user is None:
            return _get_response(
                "User with email {} not present".format(json["email"]), 400
            )
        return _get_response(user.serialize(), 200)
    return _get_response("Resource not found", 400)


# --------- END API definition --------------------------
logging.basicConfig(level=logging.DEBUG)
db_session = init_db("sqlite:///user.db")
app = connexion.App(__name__)
app.add_api("swagger.yml")
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


def _init_flask_app(flask_app, conf_type: str = "config.DebugConfiguration"):
    """
    This method init the flask app
    :param flask_app:
    """
    flask_app.config.from_object(conf_type)
    if "TestConfiguration" in conf_type:
        global db_session
        db_session = init_db("sqlite:///tests/user.db")


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    _init_flask_app(application)
    app.run(port=5002)
