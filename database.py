from sqlalchemy import create_engine, Column, Integer, Float, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = declarative_base()


class Restaurant(db):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text(100)) 
    likes = Column(Integer) # will store the number of likes, periodically updated in background
    lat = Column(Float) # restaurant latitude
    lon = Column(Float) # restaurant longitude
    phone = Column(Text(50))

    def serialize(self):
        return dict([(k,v) for k,v in self.__dict__.items() if k[0] != '_'])

def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                             bind=engine))
    db.query = db_session.query_property()
    db.metadata.create_all(bind=engine)
    

    q = db_session.query(Restaurant).filter(Restaurant.id == 1)
    restaurant = q.first()
    if restaurant is None:
        example = Restaurant()
        example.name = 'Trial Restaurant'
        example.likes = 42
        example.phone = 555123456
        example.lat = 43.720586
        example.lon = 10.408347
        db_session.add(example)
        db_session.commit()

    return db_session
