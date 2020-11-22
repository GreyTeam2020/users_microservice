import logging

from utils import Utils
from services import UserService


class Test_Components:
    """
    This test include the component testing that
    help us to test the answer from the client
    """

    def test_create_customer_ok(self, client, db):
        """
        This test function include the logic to test the
        client test and test the response that should be correct

        Test Flow:
        - Generate the correct JSON with python map
        - user Utils function to make the request with the flask test function
        - test the code response
        - clean the database
        """
        json = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        response = Utils.register_user(client, json, 3)
        aspected_response = Utils.reproduce_json_response("OK")
        assert response.status_code == 200
        assert aspected_response["result"] in response.data.decode("utf-8")

        Utils.del_user_on_db_with_email(db, json["email"])
        user = Utils.get_user_on_db_with_email(db, json["email"])
        assert user is None

    def test_create_customer_ko(self, client, db):
        """
        This test function include the logic to test the
        client test and test the response that should be correct

        Test Flow:
        - Generate the correct JSON with python map
        - user Utils function to make the request with the flask test function
        - test the code response
        - clean the database
        """
        json = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        response = Utils.register_user(client, json, 3)
        assert response.status_code != 200

        user = Utils.get_user_on_db_with_email(db, json["email"])
        assert user is None

    def test_create_customer_ko_user_already_exist(self, client, db):
        """
        This test function include the logic to test the
        client test and test the response that should be correct

        Test Flow:
        - Generate the correct JSON with python map
        - user Utils function to make the request with the flask test function
        - test the code response
        - clean the database
        """
        json = {
            "firstname": "Home",
            "lastname": "Simpson",
            "password": "Alibaba",
            "phone": "80008000",
            "dateofbirth": "1984-12-12",
            "email": "homer@me.edu",
        }
        response = Utils.register_user(client, json, 3)
        assert response.status_code == 200
        assert "OK" in response.data.decode("utf-8")

        response = Utils.register_user(client, json, 3)
        assert response.status_code == 412

        Utils.del_user_on_db_with_email(db, json["email"])

    def test_login_user_ok(self, client, db):
        """
        This function test the perform the  request to login the user
        :param client: flask test client
        :param db: database session
        """
        json_create = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None

        json_login = {
            "email": json_create["email"],
            "password": json_create["password"],
        }
        response = Utils.login_user(client, json_login)
        user = Utils.get_user_on_db_with_email(db, json_create["email"])
        assert response.status_code == 200
        assert user.email in response.data.decode("utf-8")

        Utils.del_user_on_db_with_id(db, user.id)
        user = Utils.get_user_on_db_with_email(db, json_create["email"])
        assert user is None

    def test_login_user_ko(self, client, db):
        """
        This function test the perform the  request to login the user
        :param client: flask test client
        :param db: database session
        """
        json_login = {
            "email": "home@gmail.com",
            "password": "alibaba",
        }
        response = Utils.login_user(client, json_login)
        assert response.status_code == 404
        assert "User with email {} not present".format(
            json_login["email"]
        ) in response.data.decode("utf-8")

        user = Utils.get_user_on_db_with_email(db, json_login["email"])
        assert user is None

    def test_modify_user_ok(self, client, db):
        """
        This test method perform the request to modify the user
        :param client: flask test client
        :param db: database session
        """
        json = {
            "firstname": "Bart",
            "lastname": "Simpson",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        user = UserService.create_user(db, json)
        assert user is not None

        json["firstname"] = "Homer"
        json["role"] = user.role_id
        json["id"] = user.id

        response = Utils.modify_user(client, json)
        logging.debug(response.data)
        user = Utils.get_user_on_db_with_email(db, json["email"])
        assert response.status_code == 200
        assert "Homer" in response.data.decode("utf-8")
        assert "Bart" not in response.data.decode("utf-8")

        Utils.del_user_on_db_with_id(db, user.id)
        user = Utils.get_user_on_db_with_email(db, json["email"])
        assert user is None

    def test_modify_user_ko(self, client, db):
        """
        This test method perform the request to modify the user
        :param client: flask test client
        :param db: database session
        """
        json = {
            "firstname": "Bart",
            "lastname": "Simpson",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        json["role"] = 3
        json["id"] = 20

        response = Utils.modify_user(client, json)
        assert response.status_code == 404
        assert "Resource not found" in response.data.decode("utf-8")

        user = Utils.get_user_on_db_with_email(db, json["email"])
        assert user is None

    def test_delete_user_ok(self, client, db):
        """
        This test method perform the request to modify the user
        :param client: flask test client
        :param db: database session
        """
        json = {
            "firstname": "Bart",
            "lastname": "Simpson",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        user = UserService.create_user(db, json)
        assert user is not None

        json_login = {
            "email": json["email"],
            "password": json["password"],
        }
        response = Utils.login_user(client, json_login)

        response = Utils.delete_user(client, user.id)
        assert response.status_code == 200
        assert "OK" in response.data.decode("utf-8")

        user = Utils.get_user_on_db_with_email(db, json["email"])
        assert user is None

    def test_delete_user_ko(self, client, db):
        """
        This test method perform the request to modify the user
        :param client: flask test client
        :param db: database session
        """
        response = Utils.delete_user(client, 20)
        assert response.status_code == 404
        assert "User doesn't exist" in response.data.decode("utf-8")

    def test_check_user_ok(self, client, db):
        """
        This function test the perform the  request to login the user
        :param client: flask test client
        :param db: database session
        """
        json_create = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None

        json = {
            "email": json_create["email"],
        }
        response = Utils.check_user(client, json)
        assert response.status_code == 200
        assert user.email in response.data.decode("utf-8")

        json = {
            "phone": json_create["phone"],
        }
        response = Utils.check_user(client, json)
        assert response.status_code == 200
        assert user.phone in response.data.decode("utf-8")

        Utils.del_user_on_db_with_id(db, user.id)
        user = Utils.get_user_on_db_with_email(db, json_create["email"])
        assert user is None

    def test_check_user_ko(self, client, db):
        """
        This function test the perform the  request to login the user
        :param client: flask test client
        :param db: database session
        """
        json_create = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }

        json = {
            "email": json_create["email"],
        }
        response = Utils.check_user(client, json)
        assert response.status_code == 404

        json = {
            "phone": json_create["phone"],
        }
        response = Utils.check_user(client, json)
        assert response.status_code == 404

    def test_get_role_by_id(self, client, db):
        """
        TODO implement the test to check if the method to
        get the role by id work
        :param client:
        :param db:
        :return:
        """
        pass

    def test_get_user_by_id(self, client, db):
        """
        Test flow:
        - Create User
        - Get user by id
        - check user
        - clean db
        :param client: flask test client
        :param db: db session
        """
        json_create = {
            "firstname": "Vincenzo",
            "lastname": "Palazzo",
            "password": "Alibaba",
            "phone": "100023",
            "dateofbirth": "1996-12-12",
            "email": "alibaba@alibaba.it",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None

        response = Utils.get_user_by_id(client, user.id)
        assert response.status_code == 200
        json = response.data.decode("utf-8")
        assert user.firstname in json
        assert user.phone in json
        assert user.email in json
        assert str(user.role_id) in json

        Utils.del_user_on_db_with_id(db, user.id)
        user = Utils.get_user_on_db_with_email(db, json_create["email"])
        assert user is None

    def test_unmark_positive_customer_email(self, client, db):
        """
        To test unmark of a positive customer
        """

        # mark a user as a positive
        # unmark user by email (key = email)
        # check the user is not positive
        pass

    def test_unmark_positive_customer_phone(self, client, db):
        # mark a user as a positive
        # unmark user by phone (key=phone)
        # check the user is not positive
        pass

    def test_unmark_positive_customer_wrong_key(self, client, db):
        """
        To test unmark of a customer using a wronk key
        """
        body = {"key": "wrong", "value": "example@email.com"}
        response = client.put("/user/unmark", json=body, follow_redirects=True)
        assert response.status_code == 400
        json_data = response.json
        assert json_data["result"] == "Bad Request"

    def test_unmark_positive_customer_wrong_value_email(self, client, db):
        body = {"key": "email", "value": "abcdefg3"}
        response = client.put("/user/unmark", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["result"] == "User not found"

    def test_unmark_positive_customer_wrong_value_phone(self, client, db):
        body = {"key": "phone", "value": "abcdefg3"}
        response = client.put("/user/unmark", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["result"] == "User not found"

    def test_unmark_customer_that_not_exists(self, client, db):
        body = {"key": "email", "value": "example@email.com"}

        response = client.put("/user/unmark", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["result"] == "User not found"

    def test_unmark_positive_customer_email(self, client, db):
        """
        To test unmark of a positive customer
        """

        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None
        response = UserService.mark_user_as_positive(db, user.email, "")
        assert response is True

        body = {"key": "email", "value": user.email}
        response = client.put("/user/unmark", json=body, follow_redirects=True)
        positive = UserService.user_is_positive(db, user.id)
        assert positive is None

        Utils.del_user_on_db_with_id(db, user.id)

    def test_unmark_positive_customer_phone(self, client, db):

        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None
        response = UserService.mark_user_as_positive(db, "", user.phone)
        assert response is True

        body = {"key": "phone", "value": user.phone}
        response = client.put("/user/unmark", json=body, follow_redirects=True)
        positive = UserService.user_is_positive(db, user.id)
        assert positive is None

        Utils.del_user_on_db_with_id(db, user.id)

    def test_unmark_a_not_customer(self, client, db):

        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create, 2)
        assert user is not None

        body = {"key": "email", "value": user.email}
        response = client.put("/user/unmark", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["result"] == "User not found"

        Utils.del_user_on_db_with_id(db, user.id)

    def test_unmark_a_not_positive(self, client, db):

        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None

        body = {"key": "email", "value": user.email}
        response = client.put("/user/unmark", json=body, follow_redirects=True)
        assert response.status_code == 404
        json_data = response.json
        assert json_data["result"] == "User not positive"

        Utils.del_user_on_db_with_id(db, user.id)

    def test_check_a_not_positive_customer(self, client, db):

        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None

        response = client.get(
            "/user/checkpositive/email/" + str(user.email), follow_redirects=True
        )

        assert response.status_code == 200
        json_data = response.json
        assert json_data["result"] == "Not positive"

        Utils.del_user_on_db_with_id(db, user.id)

    def test_check_a_positive_customer_email(self, client, db):

        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None
        response = UserService.mark_user_as_positive(db, user.email, "")
        assert response is True

        response = client.get(
            "/user/checkpositive/email/" + str(user.email), follow_redirects=True
        )

        assert response.status_code == 200
        json_data = response.json
        assert json_data["result"] == "Positive"

        Utils.del_user_on_db_with_id(db, user.id)

    def test_check_a_positive_customer_phone(self, client, db):

        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None
        response = UserService.mark_user_as_positive(db, "", user.phone)
        assert response is True

        response = client.get(
            "/user/checkpositive/phone/" + str(user.phone), follow_redirects=True
        )

        assert response.status_code == 200
        json_data = response.json
        assert json_data["result"] == "Positive"

        Utils.del_user_on_db_with_id(db, user.id)

    def test_info_not_positive_customer(self, client, db):
        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None

        response = client.get(
            "/user/positiveinfo/email/" + str(user.email), follow_redirects=True
        )

        assert response.status_code == 404
        json_data = response.json
        assert json_data["result"] == "Information not found"

        Utils.del_user_on_db_with_id(db, user.id)

    def test_info_positive_customer_email(self, client, db):
        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None
        response = UserService.mark_user_as_positive(db, user.email, "")
        assert response is True

        response = client.get(
            "/user/positiveinfo/email/" + str(user.email), follow_redirects=True
        )
        assert response.status_code == 200

        Utils.del_user_on_db_with_id(db, user.id)

    def test_info_positive_customer_phone(self, client, db):
        json_create = {
            "firstname": "Bobby",
            "lastname": "Bishop",
            "password": "bobbyb",
            "phone": "123456789",
            "dateofbirth": "1985-05-19",
            "email": "bobbyb@email.com",
        }
        user = UserService.create_user(db, json_create)
        assert user is not None
        response = UserService.mark_user_as_positive(db, "", user.phone)
        assert response is True

        response = client.get(
            "/user/positiveinfo/phone/" + str(user.phone), follow_redirects=True
        )
        assert response.status_code == 200

        Utils.del_user_on_db_with_id(db, user.id)

    def test_mark_positive(self, client, db):
        pass

    def test_report_positive_after_one(self, client, db):
        pass

    def test_report_positive_zero(self, client, db):
        pass
