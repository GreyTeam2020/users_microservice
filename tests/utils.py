from random import randrange

from database import User
from services import UserService


class Utils:
    """
    This class contains all logic to implement the client request
    to make a simple component test.
    """

    @staticmethod
    def reproduce_json_response(message: str, is_custom_obj: bool = False):
        if is_custom_obj is False:
            return {"result": message}
        return message

    @staticmethod
    def get_json_about_new_user(
        name: str = "user_{}".format(randrange(100000)),
        lastname: str = "user_{}".format(randrange(100000)),
        password: str = "pass_{}".format(randrange(100000)),
        phone: str = "349{}".format(randrange(100000)),
    ):
        """
        This method return the json about the new user
        :param name: name user (optional)
        :param lastname: lastname user (option)
        :param password: password (optional)
        :param phone: phone (optional)
        :return: python map with data about the new user
        """
        return {
            "firstname": name,
            "lastname": lastname,
            "password": password,
            "phone": phone,
            "dateofbirth": "1996-12-12",
            "email": "{}@gmail.com".format(name),
        }

    @staticmethod
    def register_user(client, json_data, role_id: int):
        """
        This method perform the request to register a new user
        :param client: Is a flask app created inside the fixtures
        :param user: Is the User form populate with the mock data
        :return: response from URL "/user/create_user"
        """
        if role_id == 3:
            return client.post(
                "/user/create_operator", json=json_data, follow_redirects=True
            )
        return client.post("/user/create_user", json=json_data, follow_redirects=True)

    @staticmethod
    def login_user(client, json_data):
        """
        This method perform the request to register a new user
        :param client: Is a flask app created inside the fixtures
        :param user: Is the User form populate with the mock data
        :return: response from URL "/user/create_user"
        """
        return client.post("/user/login", json=json_data, follow_redirects=True)

    @staticmethod
    def check_user(client, json_data):
        """
        This method perform the request to register a new user
        :param client: Is a flask app created inside the fixtures
        :param user: Is the User form populate with the mock data
        :return: response from URL "/user/create_user"
        """
        if "email" in json_data:
            return client.post("/user/user_by_email", json=json_data, follow_redirects=True)
        return client.post("/user/user_by_phone", json=json_data, follow_redirects=True)

    @staticmethod
    def modify_user(client, json_data):
        """
        This method perform the request to register a new user
        :param client: Is a flask app created inside the fixtures
        :param user: Is the User form populate with the mock data
        :return: response from URL "/user/data{id}"
        """
        return client.patch("/user/data/", json=json_data, follow_redirects=True)

    @staticmethod
    def delete_user(client, id):
        """
        This method perform the request to register a new user
        :param client: Is a flask app created inside the fixtures
        :param user: Is the User form populate with the mock data
        :return: response from URL "/user/data{id}"
        """
        return client.delete("/user/delete/{}".format(id), follow_redirects=True)

    @staticmethod
    def del_user_on_db_with_id(db_session, user_id: int):
        """
        This method contains the code to delete a user on database with id
        :param db_session: database session
        :param user_id: user id
        """
        db_session.query(User).filter_by(id=user_id).delete()
        db_session.commit()

    @staticmethod
    def del_user_on_db_with_email(db_session, email_user: str):
        """
        This method contains the code to delete a user on database with id
        :param db_session: database session
        :param user_id: user id
        """
        db_session.query(User).filter_by(email=email_user).delete()
        db_session.commit()

    @staticmethod
    def get_user_on_db_with_email(db_session, email_user: str):
        """
        This method contains the code to delete a user on database with id
        :param db_session: database session
        :param user_id: user id
        """
        return db_session.query(User).filter_by(email=email_user).first()

# --------------------------- UTil function to make operation with Database --------------------------

    @staticmethod
    def create_user_on_db(db_session, ran: int = randrange(100000)):
        json = {
            "firstname": "User_{}".format(ran),
            "lastname": "user_{}".format(ran),
            "password": "Alibaba{}".format(ran),
            "phone": "1234562344{}".format(ran),
            "dateofbirth": "12/12/2000",
            "email": "alibaba{}@alibaba.com".format(str(ran)),
        }
        return UserService.create_user(db_session, json)
