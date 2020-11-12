import logging
from datetime import datetime

from flask import current_app

from database import User, Positive, Role


class UserService:
    """
    This service is a wrapper of all operation with user
    - create a new user
    - deleter a user if exist
    """

    @staticmethod
    def create_user(db_session, request, role_id: int = 3):
        """
        :return:
        """
        new_user = User()
        new_user.email = request.get_json("email")
        current_app.logger.debug("Email user: {}".format(new_user.email))
        new_user.firstname = request.get_json("firstname")
        current_app.logger.debug("First name {}".format(new_user.firstname))
        new_user.lastname = request.get_json("lastname")
        current_app.logger.debug("Last name {}".format(new_user.lastname))
        password = request.get_json("password")
        current_app.logger.debug("User password {}".format(password))
        new_user.phone = request.get_json("phone")
        current_app.logger.debug("Phone {}".format(new_user.phone))
        new_user.dateofbirth = datetime.now()
        #logging.debug("dateofbirth: {}".format(new_user.dateofbirth))
        new_user.role_id = role_id
        new_user.set_password(password)
        db_session.add(new_user)
        db_session.commit()
        return db_session.query(User).filter_by(email=new_user.email)
