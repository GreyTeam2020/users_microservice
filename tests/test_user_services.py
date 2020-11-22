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
            "dateofbirth": "1996-12-12",
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
            "dateofbirth": "1996-12-12",
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
            "dateofbirth": "1996-12-12",
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
            "dateofbirth": "1996-12-12",
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
        json["id"] = user.id
        user = UserService.modify_user(db, json)
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
        json["id"] = 1
        user = UserService.modify_user(db, json)
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

    def test_get_user_by_email(self, db):
        """
        This function contains the code to test the
        user service tha allows to retetrive the user having the email
        :param db: database session
        """
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3

        assert UserService.get_user_by_email(db, user.email).id == user.id

        is_delete = UserService.delete_user(db, user.id)
        assert is_delete is True

    def test_mark_user_as_covid_positive(self, db):
        """
        This function test try to discover fault inside the
        mark postivive function inside the USerServices

        Flow tests is:
        - Create a new User
        - Mark this user as positive
        - check if the user if positive on the table
        - clean db (remove the user and the positive)
        """
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3

        success_mark = UserService.mark_user_as_positive(
            db, json["email"], json["phone"]
        )
        assert success_mark is True

        Utils.del_user_on_db_with_id(db, user.id)
        user = Utils.del_user_on_db_with_id(db, user.id)
        assert user is None

    def test_unmark_user_as_covid_positive(self, db):
        """
        This function test try to discover fault inside the
        mark postivive function inside the USerServices

        Flow tests is:
        - Create a new User
        - Mark this user as positive
        - check if the user if positive on the table
        - clean db (remove the user and the positive)
        """
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3

        success_mark = UserService.mark_user_as_positive(
            db, json["email"], json["phone"]
        )
        assert success_mark is True

        success_unmark = UserService.unmark_user_as_not_positive(db, user.id)
        assert success_unmark is True

        Utils.del_user_on_db_with_id(db, user.id)
        user = Utils.del_user_on_db_with_id(db, user.id)
        assert user is None

    def test_report_positive_after_one(self, db):
        json = Utils.get_json_about_new_user()
        user = UserService.create_user(db, json)
        assert user is not None
        assert user.role_id is 3
        success_mark = UserService.mark_user_as_positive(
            db, json["email"], json["phone"]
        )
        assert success_mark is True

        users = UserService.report_positive(db)
        assert len(users) == 1

        success_unmark = UserService.unmark_user_as_not_positive(db, user.id)
        assert success_unmark is True
        Utils.del_user_on_db_with_id(db, user.id)
        user = Utils.del_user_on_db_with_id(db, user.id)
        assert user is None

    def test_report_positive_zero(self, db):
        users = UserService.report_positive(db)
        assert len(users) == 0
