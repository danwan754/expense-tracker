# test_app_processes.py

import unittest
import os

from flask_testing import TestCase
from flask import abort, url_for

from app import create_app, db
from app.models import User, Budget, Expense


class TestBase(TestCase):

    TEST_DB = 'test.db'
    test_email = 'test_email@gmail.com'
    test_password = 'test_password'


    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.getcwd(), self.TEST_DB)
        )
        return app


    def setUp(self):
        db.create_all()
        user = User(email=self.test_email, password=self.test_password)
        db.session.add(user)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    ########################
    #### helper methods ####
    ########################

    def register(self, email, password, confirm_password):
        return self.client.post(
            url_for('auth.register'),
            data=dict(email=email, password=password, confirm_password=confirm_password),
            follow_redirects=False
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )


class TestAuthentication(TestBase):

    def test_valid_user_registration(self):
        """
        Test that successful registration redirects to login page, display
        flash message, and adds user to database
        """

        response = self.register("test_email_2@gmail.com", "test_password_2", "test_password_2")
        self.assertEqual(User.query.count(), 2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url_for('auth.login'))


    # def test_invalid_user_registration_different_passwords(self):
    #     """
    #     Test that registering with different password and password confirmation
    #     will render same registration page
    #     """
    #
    #     response = self.register('test_email_2@gmail.com', 'testPassword', 'differentPassword')
    #     # self.assertIn(b'Field must be equal to password.', response.data)
    #     self.assertEqual(response.status_code, 200)



class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in User table
        """

        self.assertEqual(User.query.count(), 1)


    def test_budget_model(self):
        """
        Test number of records in Budget table
        """

        self.assertEqual(Budget.query.count(), 0)
        budget = Budget(daily=40, user_id=1)
        db.session.add(budget)
        db.session.commit()
        self.assertEqual(Budget.query.count(), 1)


    def test_expense_model(self):
        """
        Test number of records in Expense table
        """

        self.assertEqual(Expense.query.count(), 0)
        expense = Expense(item="coffee", cost="2.00", category="Food", user_id=1)
        db.session.add(expense)
        db.session.commit()
        self.assertEqual(Expense.query.count(), 1)


class TestViews(TestBase):

    def test_home_view_while_logged_out(self):
        """
        Test that home page is accessible without logging in
        """

        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)


    def test_login_view_while_logged_out(self):
        """
        Test that login page is accessible without logging in
        """

        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)


    def test_logout_view_while_logged_out(self):
        """
        Test that logout page is inaccessible without logging in and redirects
        to login page then to logout page
        """

        targeted_url = url_for('auth.logout')
        redirected_url = url_for('auth.login', next=targeted_url)
        response = self.client.get(targeted_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirected_url)


    def test_dashboard_view_while_logged_out(self):
        """
        Test that the dashboard is inaccessible without logging in and redirects
        to login page then to dashboard
        """

        targeted_url = url_for('home.dashboard')
        redirected_url = url_for('auth.login', next=targeted_url)
        response = self.client.get(targeted_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirected_url)


    # def test_home_view_while_logged_in(self):
    #     """
    #     Test that home page is accessible while logged in
    #     """
    #
    #
    #     response = self.client.get(url_for('home.homepage'))
    #     self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
