from datetime import datetime
import logging
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Text,
    Unicode,
    DateTime,
    Boolean,
    ForeignKey,
    Date,
)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

db = declarative_base()


class User(db):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Unicode(128), nullable=False, unique=True)
    phone = Column(Unicode(16), nullable=False, unique=True)
    firstname = Column(Unicode(128))
    lastname = Column(Unicode(128))
    _password = Column(Unicode(128))
    dateofbirth = Column(DateTime)

    _is_active = Column(Boolean, default=True)
    _is_admin = Column(Boolean, default=False)
    # user role
    role_id = Column(Integer, ForeignKey("role.id"))
    restaurant = relationship("Role", foreign_keys="User.role_id")
    _is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self._password = generate_password_hash(password)
        logging.debug("Pass wit hash {}".format(self._password))

    def set_role(self, role):
        self._role = role

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        logging.debug("Pass before check {}".format(password))
        checked = check_password_hash(self._password, password)
        self._authenticated = checked
        logging.debug("Pass after check {}".format(checked))
        return self._authenticated

    def get_id(self):
        return self.id

    def serialize(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != "_"])


class Role(db):
    # this is the role of a user (like operator, customer....)
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Text(100))
    label = Column(Text(100))

    def serialize(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != "_"])


class Positive(db):
    # all covid positives
    __tablename__ = "positive"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(Date)
    marked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", foreign_keys="Positive.user_id")

    def serialize(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != "_"])

def init_db(uri):
    engine = create_engine(uri)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    db.query = db_session.query_property()
    db.metadata.create_all(bind=engine)
    
    q = db_session.query(User).filter(User.email == "john.doe@email.com")
    user = q.first()
    if user is None:
        first_customer = User()
        first_customer.firstname = "John"
        first_customer.lastname = "Doe"
        first_customer.email = "john.doe@email.com"
        first_customer.phone = "111234765"
        first_customer.is_admin = False
        first_customer.set_password("customer")
        first_customer.role_id = 3
        db_session.add(first_customer)
        db_session.commit()

    q = db_session.query(User).filter(User.email == "ham.burger@email.com")
    user = q.first()
    if user is None:
        first_operator = User()
        first_operator.firstname = "Ham"
        first_operator.lastname = "Burger"
        first_operator.email = "ham.burger@email.com"
        first_operator.phone = "222333567"
        first_operator.is_admin = False
        first_operator.set_password("operator")
        first_operator.role_id = 2
        db_session.add(first_operator)
        db_session.commit()

    q = db_session.query(User).filter(User.email == "nick.miller@email.com")
    user = q.first()
    if user is None:
        second_operator = User()
        second_operator.firstname = "Nick"
        second_operator.lastname = "Miller"
        second_operator.email = "nick.miller@email.com"
        second_operator.phone = "119385729"
        second_operator.is_admin = False
        second_operator.set_password("nickmiller")
        second_operator.role_id = 2
        db_session.add(second_operator)
        db_session.commit()

    q = db_session.query(User).filter(User.email == "health_authority@gov.com")
    user = q.first()
    if user is None:
        health_authority = User()
        health_authority.firstname = "Health"
        health_authority.lastname = "Authority"
        health_authority.email = "health_authority@gov.com"
        health_authority.phone = "321456783"
        health_authority.is_admin = False
        health_authority.set_password("nocovid")
        health_authority.role_id = 4
        db_session.add(health_authority)
        db_session.commit()
    

    # create the user roles
    q = db_session.query(Role).filter(Role.id == 1)
    role = q.first()
    if role is None:
        role = Role()
        role.value = "ADMIN"
        role.label = "Admin role"
        db_session.add(role)
        role = Role()
        role.value = "OPERATOR"
        role.label = "Operator role"
        db_session.add(role)
        role = Role()
        role.value = "CUSTOMER"
        role.label = "Customer role"
        db_session.add(role)
        role = Role()
        role.value = "HEALTH"
        role.label = "Health role"
        db_session.add(role)
        db_session.commit()

    return db_session
