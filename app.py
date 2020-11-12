import connexion, logging, database
from flask import jsonify, request

db_session = None

def get_restaurants():  
    q = db_session.query(database.Restaurant).all()
    return [p.serialize() for p in q]

def get_restaurant(restaurant_id):  
    q = db_session.query(database.Restaurant).filter_by(id=restaurant_id).first()
    if q is None:
        return {"result": "Restaurant with id {} is not found".format(restaurant_id)}
    return q.serialize()



logging.basicConfig(level=logging.INFO)
db_session = database.init_db('sqlite:///restaurant.db')
app = connexion.App(__name__)
app.add_api('swagger.yml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=8080)