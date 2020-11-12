import connexion
from database import User, db_session, init_db
import logging
from flask import request
from services.user_service import UserService

def create_user():
    """

    :return:
    """
    user = User()
    user.email = request.get_json("email")
    logging.debug("Email user: {}".format(user.email))
    user.firstname = request.get_json("firstname")
    logging.debug("First name {}".format(user.firstname))
    user.lastname = request.get_json("lastname")
    logging.debug("Last name {}".format(user.lastname))
    password = request.get_json("password")
    logging.debug("User password {}".format(password))
    user.phone = request.get_json("phone")
    logging.debug("Phone {}".format(user.phone))
    user.dateofbirth = request.get_json("dateofbirth")
    logging.debug("dateofbirth: {}".format(user.dateofbirth))
    user = UserService.create_user(user, password=password)
    if user is not None:
        return {"result": "OK"}, 200
    return {}, 400


logging.basicConfig(level=logging.INFO)
init_db("sqlite:///user.db")
app = connexion.App(__name__)
app.add_api("swagger.yml")
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


def _init_flask_app(flask_app):
    """
    This method init the flask app
    :param flask_app:
    """
    flask_app.config.from_object("config.DebugConfiguration")

"""
@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
"""

if __name__ == "__main__":
    _init_flask_app(application)
    app.run(port=5002)
