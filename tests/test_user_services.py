from services import UserService
from database import User
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
