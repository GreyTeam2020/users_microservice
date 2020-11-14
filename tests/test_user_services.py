from services import UserService
from database import User, Role
from utils import Utils


class Test_UserServices:
    """
    This test suite test the services about user use case.
    All the code tested inside this class is inside the services/test_user_services.py
    """

    def test_create_customer(self, db):
        """
        This test try to test the simple operation to create a new operator

         Test flow:
         - Make the JSON object with the correct data
         - user the UserService to share the request
         - clean DB
        """
        json = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "12/12/1996",
            "email": "alibaba@alibaba.it",
        }
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3

        Utils.del_user_on_db_with_id(db, user.id)

    def test_create_operator(self, db):
        """
        This test try to test the simple operation to create a new operator

         Test flow:
         - Make the JSON object with the correct data
         - user the UserService to share the request
         - clean DB
        """
        json = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "345432234",
            "dateofbirth": "12/12/1996",
            "email": "alibaba@alibaba.com",
        }
        user = UserService.create_user(db, json, 2)
        assert user is not None
        assert user.role_id is not 3
        assert user.role_id is 2

        db.query(User).filter_by(id=user.id).delete()
        db.commit()

    def test_user_is_present_by_email(self, db):
        """
        This test try to test the simple operation to create a new operator

         Test flow:
         - Make the JSON object with the correct data
         - user the UserService to share the request
         - clean DB
        """
        json = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "345432234",
            "dateofbirth": "12/12/1996",
            "email": "alibaba@alibaba.com",
        }
        user = UserService.create_user(db, json, 2)
        assert user is not None
        assert user.role_id is not 3
        assert user.role_id is 2

        user = UserService.user_is_present(db, json["email"])
        assert user is not None

        Utils.del_user_on_db_with_id(db, user.id)

    def test_user_is_present_by_phone(self, db):
        """
        This test try to test the simple operation to create a new operator

         Test flow:
         - Make the JSON object with the correct data
         - user the UserService to share the request
         - clean DB
        """
        json = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "345432234",
            "dateofbirth": "12/12/1996",
            "email": "alibaba@alibaba.com",
        }
        user = UserService.create_user(db, json, 2)
        assert user is not None
        assert user.role_id is not 3
        assert user.role_id is 2

        user = UserService.user_is_present(db, phone=json["phone"])
        assert user is not None

        Utils.del_user_on_db_with_id(db, user.id)

    def test_user_is_present_not_present(self, db):
        """
        This test try to test the simple operation to create a new operator

         Test flow:
         - Make the JSON object with the correct data
         - user the UserService to share the request
         - clean DB
        """
        json = Utils.get_json_about_new_user()
        user = UserService.user_is_present(db, phone=json["phone"])
        assert user is None

    def test_user_login_ok(self, db):
        """
        This function contains the code to test the
        User services about the login, and I will aspect a good result.
        :param db: database session
        """
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3

        user = UserService.user_login(db, user.email, json["password"])
        assert user is not None
        assert user.is_authenticated is True

        Utils.del_user_on_db_with_id(db, user.id)

    def test_user_login_ko(self, db):
        """
        This function contains the code to test the
        User services about the login, and I will aspect a good result.
        :param db: database session
        """
        json = Utils.get_json_about_new_user()

        user = UserService.user_login(db, json["email"], json["password"])
        assert user is None

    def test_user_modify_ok(self, db):
        """
        This function contains the code to test the
        User services about the login, and I will aspect a good result.
        :param db: database session
        """
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3

        user = UserService.user_login(db, json["email"], json["password"])

        json["firstname"] = "Bart"
        json["role"] = user.role_id
        user = UserService.modify_user(db, json, user.id)
        assert user is not None
        assert user.firstname == "Bart"
        Utils.del_user_on_db_with_id(db, user.id)

    def test_user_modify_ko(self, db):
        """
        This function contains the code to test the
        User services about the login, and I will aspect a good result.
        :param db: database session
        """
        json = Utils.get_json_about_new_user()
        json["role"] = 3
        json["firstname"] = "Bart"
        user = UserService.modify_user(db, json, 1)
        assert user is None

    def test_user_delete_ok(self, db):
        """
        This function contains the code to test the
        User services about the login, and I will aspect a good result.
        :param db: database session
        """
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3
        user = UserService.user_login(db, user.email, json["password"])
        is_delete = UserService.delete_user(db, user.id)
        assert is_delete is True

        user = Utils.get_user_on_db_with_email(db, user.email)
        assert user is None

    def test_user_delete_ko(self, db):
        """
        This function contains the code to test the
        User services about the login, and I will aspect a good result.
        :param db: database session
        """
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3

        is_delete = UserService.delete_user(db, user.id)
        assert is_delete is False

        user = Utils.get_user_on_db_with_email(db, user.email)
        assert user is not None

    def test_get_role(self, db):
        """
        This function contains the code to test the
        user service tha allows to retetrive the role with id given
        :param db: database session
        """
        last_role = db.query(Role).order_by(Role.id.desc()).first()
        role = Role()
        role.value = "CAMALEONTE"
        role.label = "CAMALEONTE"
        db.add(role)
        db.commit()

        role = UserService.get_role_value(db, last_role.id + 1)
        assert role.value == "CAMALEONTE"

        db.query(Role).filter_by(id=role.id).delete()
        db.commit()
