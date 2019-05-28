# test_app_processes.py

import unittest
import os
from datetime import datetime, timedelta

from flask_testing import TestCase
from flask import abort, url_for

from app import create_app, db
from app.models import User, Budget, Expense
from app import app_processes


class TestBase(TestCase):

    TEST_DB = 'test.db'
    email = 'test_email@gmail.com'
    password = 'test_password'
    user_id = 1


    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.getcwd(), self.TEST_DB)
        )
        return app


    def setUp(self):
        db.create_all()
        user = User(email=self.email, password=self.password)
        db.session.add(user)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()



class TestAppProcesses(TestBase):

    #####
    # Helper methods
    #####

    def create_budget(self, user_id, dailyBudget, creationDate):
        """
        Returns a budget object
        """

        budget = Budget(user_id=user_id,
                        daily=dailyBudget,
                        creation_date=creationDate)

        return budget


    def create_and_save_expense(self, user_id, item, cost, category, date):
        """
        Create an expense object and save it to database
        """

        expense = Expense(user_id=user_id,
                          item=item,
                          cost=cost,
                          category=category,
                          date=date)
        db.session.add(expense)
        db.session.commit()


    def get_user_id(self, email):
        """
        Return user id
        """

        return User.query.with_entities(User.id).filter_by(email=email).scalar()



class TestGetTodayBudgetRemaining(TestAppProcesses):

    dailyBudget = 50

    def test_getTodayBudgetRemaining_with_no_expenses(self):
        """
        Test that today's remaining budget is fully available with no expenses
        today, but an expense for yesterday exists
        """

        expected = self.dailyBudget
        cost = 2.50
        date = datetime.now().date() - timedelta(days=1)

        budget = self.create_budget(self.user_id, self.dailyBudget, datetime.now().date())
        self.create_and_save_expense(self.user_id, "coffee", cost, "Food", date)

        todayBudgetRemaining = app_processes.getTodayBudgetRemaining(budget, self.user_id)
        self.assertEqual(todayBudgetRemaining, expected)


    def test_getTodayBudgetRemaining_with_expenses(self):
        """
        Test that today's remaining budget is partially available with expenses
        today
        """

        cost1 = 2.50
        cost2 = 12.25
        date = datetime.now().date()

        # expected = 50 - 2.50 - 12.25 = 35.25
        expected = self.dailyBudget - cost1 - cost2

        budget = self.create_budget(self.user_id, self.dailyBudget, datetime.now().date())
        self.create_and_save_expense(self.user_id, "coffee", cost1, "Food", date)
        self.create_and_save_expense(self.user_id, "lunch", cost2, "Food", date)

        todayBudgetRemaining = app_processes.getTodayBudgetRemaining(budget, self.user_id)
        self.assertEqual(todayBudgetRemaining, expected)



class TestGetWeekRemainingBudget(TestAppProcesses):

    dailyBudget = 50
    weekBudget = dailyBudget * 7
    cost1 = 2.50
    cost2 = 12.25

    def test_getWeekBudgetRemaining_with_today_as_start_of_week(self):
        """
        Test that this week's remaining budget is correct with the start of week
        being today and expenses exists for today and yesterday.
        Only today's expenses should be used to determine budget remaining.
        """

        today = datetime.now().date()
        budgetCreationDate = today
        expected = self.weekBudget

        budget = self.create_budget(self.user_id, self.dailyBudget, budgetCreationDate)
        weekBudgetRemaining = app_processes.getWeekBudgetRemaining(budget, self.user_id)
        self.assertEqual(weekBudgetRemaining, expected)

        date1 = datetime.now().date()
        date2 = date1 - timedelta(days=1)

        # expected = 350 - 2.50 = 347.50
        expected = self.weekBudget - self.cost1

        self.create_and_save_expense(self.user_id, "coffee", self.cost1, "Food", date1)
        self.create_and_save_expense(self.user_id, "lunch", self.cost2, "Food", date2)

        weekBudgetRemaining = app_processes.getWeekBudgetRemaining(budget, self.user_id)
        self.assertEqual(weekBudgetRemaining, expected)


    def test_getWeekBudgetRemaining_with_yesterday_as_start_of_week(self):
        """
        Test that this week's remaining budget is correct with the start of week
        being yesterday and expenses exists for yesterday and today.
        Expenses for yesterday and today should determine budget remaining.
        """

        date1 = datetime.now().date()
        date2 = datetime.now().date() - timedelta(days=1)
        budgetCreationDate = date2


        # expected = 50 - 2.50 - 12.25 = 35.25
        expected = self.weekBudget - self.cost1 - self.cost2

        budget = self.create_budget(self.user_id, self.dailyBudget, budgetCreationDate)
        self.create_and_save_expense(self.user_id, "coffee", self.cost1, "Food", date1)
        self.create_and_save_expense(self.user_id, "lunch", self.cost2, "Food", date2)

        weekBudgetRemaining = app_processes.getWeekBudgetRemaining(budget, self.user_id)
        self.assertEqual(weekBudgetRemaining, expected)


if __name__ == '__main__':
    unittest.main()
