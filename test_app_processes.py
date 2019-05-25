# test_app_processes.py

import unittest
import os
from datetime import datetime

from flask_testing import TestCase
from flask import abort, url_for

from app import create_app, db
from app.models import User, Budget, Expense
from app import app_processes


class TestBase(TestCase):

    TEST_DB = 'test.db'

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.getcwd(), self.TEST_DB)
        )
        return app


    def setUp(self):
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestAppProcesses(TestBase):

    def test_getTodayBudgetRemaining(self):
        """
        Test that today's remaining budget is correct
        """

        expected = 50

        test_email = 'test_email@gmail.com'
        test_password = 'test_password'

        user = User(email=self.test_email, password=self.test_password)
        db.session.add(user)
        db.session.commit()

        user_id = User.query.entities_with(User.id).filter_by(email=test_email)

        budget = Budget(user_id=user_id,
                        daily=50,
                        creation_date=datetime.now().date)

        todayBudgetRemaining = app_processes.getTodayBudgetRemaining(budget, user_id)

        self.assertEqual(todayBudgetRemaining, expected)



if __name__ == '__main__':
    unittest.main()
