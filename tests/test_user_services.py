from services import UserService
from database import User


class Test_UserServices:
    """
    This test suite test the services about user use case.
    All the code tested inside this class is inside the services/test_user_services.py
    """

    def test_create_user(self, db):
        """
        test create user
        :return:
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

        db.query(User).filter_by(id=user.id).delete()
        db.commit()

    def test_create_customer(self, db):
        """
        test create user
        :return:
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
