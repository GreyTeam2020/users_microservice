from datetime import datetime
from flask import current_app
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
        current_app.logger.debug("Email user: {}".format(new_user.email))
        new_user.firstname = json["firstname"]
        current_app.logger.debug("First name {}".format(new_user.firstname))
        new_user.lastname = json["lastname"]
        current_app.logger.debug("Last name {}".format(new_user.lastname))
        password = json["password"]
        current_app.logger.debug("User password {}".format(password))
        new_user.phone = json["phone"]
        current_app.logger.debug("Phone {}".format(new_user.phone))
        date_string = json["dateofbirth"]
        current_app.logger.debug("date_string: {}".format(date_string))
        new_user.dateofbirth = datetime.strptime(date_string, "%Y-%m-%d")
        current_app.logger.debug("dateofbirth: {}".format(new_user.dateofbirth))
        new_user.role_id = role_id
        new_user.set_password(password)
        db_session.add(new_user)
        db_session.flush()
        db_session.commit()
        return db_session.query(User).filter_by(email=new_user.email).first()

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
