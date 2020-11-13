import logging
from datetime import datetime
from database import User


class UserService:
    """
    This service is a wrapper of all operation with user
    - create a new user
    - deleter a user if exist
    """

    @staticmethod
    def create_user(db_session, json, role_id: int = 3):
        """
        This method help to contains the logic of the create user about microservices
        This bring all information inside a dictionary
        :param db_session: The actual db session
        :param json: a python map that contains all information about the user
        :param role_id: a role id to help chose if the user is operator (2) or customer (3)
        :raise Generic exception if the user is already present, is used the function user_is_present
        :return: the user is it is crated
        """
        new_user = User()
        new_user.email = json["email"]
        logging.debug("Email user: {}".format(new_user.email))
        new_user.firstname = json["firstname"]
        logging.debug("First name {}".format(new_user.firstname))
        new_user.lastname = json["lastname"]
        logging.debug("Last name {}".format(new_user.lastname))
        password = json["password"]
        logging.debug("User password {}".format(password))
        new_user.set_password(password)
        new_user.phone = json["phone"]
        logging.debug("Phone {}".format(new_user.phone))
        date_string = json["dateofbirth"]
        logging.debug("date_string: {}".format(date_string))
        new_user.dateofbirth = datetime.strptime(date_string, "%Y-%m-%d")
        logging.debug("dateofbirth: {}".format(new_user.dateofbirth))
        new_user.role_id = role_id
        db_session.add(new_user)
        db_session.commit()
        return db_session.query(User).filter_by(email=new_user.email).first()

    @staticmethod
    def user_is_present_with_id(db_session, user_id: int):
        """
        This method contains the logic to search a user with the
        :param user_id: user id inside the database
        :return: use user if exist otherwise, it is return None
        """
        return db_session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def user_is_present(db_session, email: str = None, phone: str = None):
        """
        This method contains the logic to search a user with the
        :param email: user email if it is present we use to filter user
        :param phone: phone number, if it is present we use to filter user
        :return: use user if exist otherwise, it is return None
        """
        if phone is not None and len(phone) != 0:
            return db_session.query(User).filter_by(phone=phone).first()
        return db_session.query(User).filter_by(email=email).first()

    @staticmethod
    def user_login(db_session, email: str, password: str):
        """
        This method contains the logic to search a user with the
        :param email: user email if it is present we use to filter user
        :param phone: phone number, if it is present we use to filter user
        :return: use user if exist otherwise, it is return None
        """
        user = db_session.query(User).filter_by(email=email).first()
        logging.debug("User from db with email {} null? {}".format(email, user is None))
        if user is not None and user.authenticate(password) is True:
            logging.debug("User with email {} ok to make a login".format(email))
            return user
        logging.debug("User with email {} not allowed to make a login".format(email))
        return None

    @staticmethod
    def modify_user(db_session, json, user_id: id):
        """
        This method take an user that is populate from te caller
        and make the operation to store it as persistent (e.g database).
        We can assume that by default is not possible change the password
        :param form: the user form with new data
        :param role_id: by default is none but it is possible setup to change also the role id
        :return: the user with the change if is changed
        """
        email = json["email"]
        date_string = json["dateofbirth"]
        logging.debug("date_string: {}".format(date_string))
        user = db_session.query(User).filter_by(id=user_id).first()
        if user is None:
            return None
        user.email = json["email"]
        user.firstname = json["firstname"]
        user.lastname = json["lastname"]
        user.dateofbirth = datetime.strptime(date_string, "%Y-%m-%d")
        user.role_id = json["role"]
        db_session.commit()
        return db_session.query(User).filter_by(email=email).first()

    @staticmethod
    def delete_user(db_session, user_id: int):
        user = db_session.query(User).filter_by(id=user_id).first()
        if user.is_authenticated() is False:
            return False
        db_session.query(User).filter_by(id=user_id).delete()
        db_session.commit()
        return True
