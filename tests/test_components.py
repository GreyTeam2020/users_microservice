from utils import Utils


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
            "dateofbirth": "12/12/1996",
            "email": "alibaba@alibaba.it",
        }
        response = Utils.register_user(client, json, 3)
        assert response.status_code == 200
        assert "OK" in response.data.decode("utf-8")

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
            "dateofbirth": "12/12/1996",
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
            "dateofbirth": "12/12/1984",
            "email": "homer@me.edu",
        }
        response = Utils.register_user(client, json, 3)
        assert response.status_code == 200
        assert "OK" in response.data.decode("utf-8")

        response = Utils.register_user(client, json, 3)
        assert response.status_code == 500

        Utils.del_user_on_db_with_email(db, json["email"])
