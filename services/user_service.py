from flask_login import current_user
from database import db_session, User, Positive, Role


class UserService:
    """
    This service is a wrapper of all operation with user
    - create a new user
    - deleter a user if exist
    """

    @staticmethod
    def create_user(new_user: User, password, role_id: int = 3):
        """

        :return:
        """
        ## By default I assume CUSTOMER
        new_user.role_id = role_id
        new_user.set_password(password)
        db_session.add(new_user)
        db_session.commit()

        q = db_session.query(User).filter(User.email == new_user.email)
        user = q.first()
        return user
