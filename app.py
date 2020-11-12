import connexion
from database import init_db
import logging
from flask import request
from services.user_service import UserService


db_session = None


def create_user():
    """
    TODO
    :return:
    """
    if request.method == "POST":
        try:
            user = UserService.create_user(db_session, request.get_json())
        except Exception as ex:
            return {"result": str(ex.message)}
        if user is not None:
            return {"result": "OK"}, 200
        else:
            return {"result": "User not created because we have an error on server"}, 500
    return {}, 400


logging.basicConfig(level=logging.INFO)
db_session = init_db("sqlite:///user.db")
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




@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    _init_flask_app(application)
    app.run(port=5002)
