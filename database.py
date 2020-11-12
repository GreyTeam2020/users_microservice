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
session = None


class User(db):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Unicode(128), nullable=False, unique=True)
    phone = Column(Unicode(16), nullable=False, unique=True)
    firstname = Column(Unicode(128))
    lastname = Column(Unicode(128))
    password = Column(Unicode(128))
    dateofbirth = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    # user role
    role_id = Column(Integer, ForeignKey("role.id"))
    restaurant = relationship("Role", foreign_keys="User.role_id")
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        # self.password = generate_password_hash(password)
        password = password

    def set_role(self, role):
        self.role = role

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id


class Role(db):
    # this is the role of a user (like operator, customer....)
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Text(100))
    label = Column(Text(100))


class Positive(db):
    # all covid positives
    __tablename__ = "positive"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(Date)
    marked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", foreign_keys="Positive.user_id")


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    global session
    session = db_session
    db.query = db_session.query_property()
    db.metadata.create_all(bind=engine)

    q = db_session.query(User).filter_by(id=1)
    restaurant = q.first()
    if restaurant is None:
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
    return db_session
