# test_app_processes.py

import unittest
import os
from datetime import datetime, timedelta, date
from calendar import monthrange

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
    cost1 = 2.50
    cost2 = 12.50

    def test_getTodayBudgetRemaining_with_no_expenses(self):
        """
        Test that today's remaining budget is fully available with no expenses
        today, but an expense for yesterday exists
        """

        expected = self.dailyBudget
        date = datetime.now().date() - timedelta(days=1)

        budget = self.create_budget(self.user_id, self.dailyBudget, datetime.now().date())
        self.create_and_save_expense(self.user_id, "coffee", self.cost1, "Food", date)

        todayBudgetRemaining = app_processes.getTodayBudgetRemaining(budget, self.user_id)
        self.assertEqual(todayBudgetRemaining, expected)


    def test_getTodayBudgetRemaining_with_expenses(self):
        """
        Test that today's remaining budget is partially available with expenses
        today
        """

        date = datetime.now().date()

        # expected = 50 - 2.50 - 12.50 = 35.00
        expected = self.dailyBudget - self.cost1 - self.cost2

        budget = self.create_budget(self.user_id, self.dailyBudget, datetime.now().date())
        self.create_and_save_expense(self.user_id, "coffee", self.cost1, "Food", date)
        self.create_and_save_expense(self.user_id, "lunch", self.cost2, "Food", date)

        todayBudgetRemaining = app_processes.getTodayBudgetRemaining(budget, self.user_id)
        self.assertEqual(todayBudgetRemaining, expected)



class TestGetWeekRemainingBudget(TestAppProcesses):

    dailyBudget = 50
    weekBudget = dailyBudget * 7
    cost1 = 2.50
    cost2 = 12.50

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


        # expected = 50 - 2.50 - 12.50 = 35.00
        expected = self.weekBudget - self.cost1 - self.cost2

        budget = self.create_budget(self.user_id, self.dailyBudget, budgetCreationDate)
        self.create_and_save_expense(self.user_id, "coffee", self.cost1, "Food", date1)
        self.create_and_save_expense(self.user_id, "lunch", self.cost2, "Food", date2)

        weekBudgetRemaining = app_processes.getWeekBudgetRemaining(budget, self.user_id)
        self.assertEqual(weekBudgetRemaining, expected)


    def test_getWeekBudgetRemaining_with_last_seven_days_ago_as_start_of_week(self):
        """
        Test that this week's remaining budget is correct with the start of week
        being 7 days ago and expenses exists 7 days ago and within 6 days ago.
        Only expenses within the last 6 days and today should determine budget remaining.
        """

        date1 = datetime.now().date() # included in this week's budget
        date2 = date1 - timedelta(days=1) # included
        date3 = date1 - timedelta(days=6) # included
        date4 = date1 - timedelta(days=7) # not included
        budgetCreationDate = date3

        budget = self.create_budget(self.user_id, self.dailyBudget, budgetCreationDate)
        self.create_and_save_expense(self.user_id, "item1", self.cost1, "category", date1)
        self.create_and_save_expense(self.user_id, "item2", self.cost1, "category", date2)
        self.create_and_save_expense(self.user_id, "item3", self.cost1, "category", date3)
        self.create_and_save_expense(self.user_id, "item4", self.cost1, "category", date4)

        # expected = 350 - 2.50 * 3 = 342.50
        expected = self.weekBudget - self.cost1 * 3

        weekBudgetRemaining = app_processes.getWeekBudgetRemaining(budget, self.user_id)
        self.assertEqual(weekBudgetRemaining, expected)



class TestGetMonthBudgetRemaining(TestAppProcesses):

    todayDate = datetime.now().date()
    dailyBudget = 50
    cost1 = 2.50
    thisMonth = todayDate.month
    thisYear = todayDate.year
    numDays = monthrange(thisYear, thisMonth)[1]
    monthBudget = dailyBudget * numDays

    if thisMonth == 1:
        prevMonth = 12
    else:
        prevMonth = thisMonth - 1

    prevMonthDate = date(todayDate.year, prevMonth, 15)

    # budgetCreationDate is arbitrary
    budgetCreationDate = prevMonthDate


    def test_getMonthBudgetRemaining_with_no_expenses_this_month(self):
        """
        Test that this month's remaining budget is full available with no expenses
        this month, but expenses exists for previous month
        """

        expected = self.monthBudget

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)
        self.create_and_save_expense(self.user_id, "item1", self.cost1, "category", self.prevMonthDate)

        monthBudgetRemaining = app_processes.getMonthBudgetRemaining(budget, self.user_id)
        self.assertEqual(monthBudgetRemaining, expected)



    def test_getMonthBudgetRemaining_with_expenses_this_month(self):
        """
        Test that this month's remaining budget is correct with an expense
        this month, but expenses exists for previous month as well.
        Only this month's expense should determine the remaining budget.
        """

        expected = self.monthBudget - self.cost1

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)
        self.create_and_save_expense(self.user_id, "item1", self.cost1, "category", self.prevMonthDate)
        self.create_and_save_expense(self.user_id, "item2", self.cost1, "category", self.todayDate)

        monthBudgetRemaining = app_processes.getMonthBudgetRemaining(budget, self.user_id)
        self.assertEqual(monthBudgetRemaining, expected)



class TestGetYearToDateSavings(TestAppProcesses):

    dailyBudget = 50
    todayDate = datetime.now().date()
    numDays = 5
    budgetCreationDate = todayDate - timedelta(days=numDays)
    expenseDate1 = budgetCreationDate + timedelta(days=1)
    expenseDate2 = budgetCreationDate + timedelta(days=4)
    expenseDate3 = budgetCreationDate + timedelta(days=5)
    cost1 = 40
    cost2 = 50
    cost3 = 60
    totalBudget = dailyBudget * numDays

    def test_getYearToDateSavings_with_no_expenses(self):
        """
        Test that savings available is the same as the sum of every daily budget
        from budget creation date to today.
        """

        expected = self.totalBudget

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)

        savings = app_processes.getYearToDateSavings(budget, self.user_id)
        self.assertEqual(savings, expected)


    def test_getYearToDateSavings_with_expenses(self):
        """
        Test that savings available is correct with expenses.
        """

        # expected = 250 - 40 - 50 = 160
        expected = self.totalBudget - self.cost1 - self.cost2

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)
        self.create_and_save_expense(self.user_id, "item1", self.cost1, "category", self.expenseDate1)
        self.create_and_save_expense(self.user_id, "item1", self.cost2, "category", self.expenseDate2)

        savings = app_processes.getYearToDateSavings(budget, self.user_id)
        self.assertEqual(savings, expected)


class TestGetMonthSavings(TestAppProcesses):

    dailyBudget = 50
    month = 6
    year = 2019
    numDays = 30
    cost = 10


    # monthBudget = 50 * 30 = 1500
    monthBudget = dailyBudget * numDays

    def test_getMonthSavings_with_no_expenses_in_month(self):
        """
        Test that the total savings in the selected month is equal to the total
        budget for that month since there are no expenses that month.
        """

        budgetCreationDate = date(2019, 4, 1)
        todayDate = date(2019, 6, 1)
        expenseDate1 = date(2019, 5, 4)
        expenseDate2 = date(2019, 4, 15)

        # expected = 1500
        expected = self.monthBudget

        budget = self.create_budget(self.user_id, self.dailyBudget, budgetCreationDate)

        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", expenseDate1)
        self.create_and_save_expense(self.user_id, "item2", self.cost, "category", expenseDate2)
        savings = app_processes.getMonthSavings(self.month, self.year, todayDate, budget, self.user_id)

        self.assertEqual(savings, expected)


    def test_getMonthSavings_with_expenses_in_month(self):
        """
        Test that the total savings in the selected month is correct when there
        are expenses that month.
        """

        budgetCreationDate = date(2019, 4, 1)
        todayDate = date(2019, 7, 1)
        expenseDate1 = date(2019, 6, 1)
        expenseDate2 = date(2019, 6, 30)

        # expected = 1500 - 10 - 10  = 1480
        expected = self.monthBudget - self.cost - self.cost

        budget = self.create_budget(self.user_id, self.dailyBudget, budgetCreationDate)

        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", expenseDate1)
        self.create_and_save_expense(self.user_id, "item2", self.cost, "category", expenseDate2)
        savings = app_processes.getMonthSavings(self.month, self.year, todayDate, budget, self.user_id)

        self.assertEqual(savings, expected)


    def test_getMonthSavings_with_expenses_and_budget_created_same_month_year(self):
        """
        Test that the total savings in the selected month is correct when the
        budget was created on the same month and year, and there are expenses.
        """

        budgetCreationDate = date(2019, 6, 5)
        todayDate = date(2019, 6, 15)
        expenseDate1 = date(2019, 6, 6)
        expenseDate2 = date(2019, 6, 14)

        # there is 11 days from June 5 to June 15, inclusive; partialBudget = 50 * 11 = 550
        partialMonthBudget = self.dailyBudget * 11

        # expected = 550 - 10 - 10  = 530
        expected = partialMonthBudget - self.cost - self.cost

        budget = self.create_budget(self.user_id, self.dailyBudget, budgetCreationDate)

        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", expenseDate1)
        self.create_and_save_expense(self.user_id, "item2", self.cost, "category", expenseDate2)
        savings = app_processes.getMonthSavings(self.month, self.year, todayDate, budget, self.user_id)

        self.assertEqual(savings, expected)


class TestGetDaySavings(TestAppProcesses):

    dailyBudget = 50
    cost = 10
    budgetCreationDate = date(2019, 6, 15)

    # arbitrary dates after budgetCreationDate
    selectedDate = date(2019, 6, 18)
    expenseDate = date(2019, 7, 15)


    def test_getDaySavings_with_no_expenses_in_selected_day(self):
        """
        Test that the total savings in selected date is correct when there are no
        expenses on that date.
        """

        # expected = 50
        expected = self.dailyBudget

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)

        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", self.expenseDate)
        savings = app_processes.getDaySavings(self.selectedDate, budget, self.user_id)

        self.assertEqual(savings, expected)


    def test_getDaySavings_with_expenses_on_selected_day(self):
        """
        Test that the total savings in the selected date is correct when there
        are expenses on that date.
        """

        # expected = 50 - 10 - 10 = 30
        expected = self.dailyBudget - self.cost - self.cost

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)

        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", self.selectedDate)
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", self.selectedDate)

        savings = app_processes.getDaySavings(self.selectedDate, budget, self.user_id)

        self.assertEqual(savings, expected)



class TestGetYearSavings(TestAppProcesses):

    year = 2019
    numDaysInYear = 365
    dailyBudget = 50
    budgetCreationDate = date(2018, 2, 1)
    cost = 10

    def test_getYearSavings_with_no_expenses_in_year(self):
        """
        Test that the total savings in the selected year is equal to the total
        budget for that year since there is not expenses that year.
        """

        # expected = 50 * 365 = 18250
        expected = self.dailyBudget * self.numDaysInYear

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)

        # this expense should not be used in the savings calculation since it is in a different year
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2018, 4, 1))

        savings = app_processes.getYearSavings(self.year, budget, self.user_id)

        self.assertEqual(savings, expected)


    def test_getYearSavings_with_expenses(self):
        """
        Test that the total savings in the selected year is correct when
        there are expenses within that year.
        """

        # expected = 50 * 365 - 10 - 10 = 18230
        expected = self.dailyBudget * self.numDaysInYear - self.cost - self.cost

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)

        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2019, 1, 1))
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2019, 12, 31))

        savings = app_processes.getYearSavings(self.year, budget, self.user_id)

        self.assertEqual(savings, expected)


    def test_getYearSavings_in_leap_year_with_expenses(self):
        """
        Test that the total savings the selected leap year is correct when
        there are expenses within that year.
        """

        # expected = 50 * 366 - 10 - 10 = 18280
        expected = self.dailyBudget * 366 - self.cost - self.cost

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)

        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2020, 1, 1))
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2020, 12, 31))

        savings = app_processes.getYearSavings(2020, budget, self.user_id)

        self.assertEqual(savings, expected)


class TestGetDateRangeSavings(TestAppProcesses):

    dailyBudget = 50
    budgetCreationDate = date(2019, 5, 1)
    cost = 10
    date1 = date(2019, 5, 30)
    date2 = date(2019, 6, 5)
    numDays = 7

    def test_getDateRangeSavings_with_expenses(self):
        """
        Test that the total savings within a date range is correct when there
        are expenses within that date range.
        """


        # expected = 50 * 7 - 10 - 10 - 10
        expected = self.dailyBudget * self.numDays - self.cost - self.cost - self.cost

        budget = self.create_budget(self.user_id, self.dailyBudget, self.budgetCreationDate)

        # these expenses are within the date range and should be included in savings calculation
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2019, 5, 30))
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2019, 6, 4))
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2019, 6, 5))


        # this expense should not be included in the calculation
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2019, 6, 6))
        self.create_and_save_expense(self.user_id, "item1", self.cost, "category", date(2019, 5, 29))


        savings = app_processes.getDateRangeSavings(self.date1, self.date2, budget, self.user_id)

        self.assertEqual(savings, expected)




if __name__ == '__main__':
    unittest.main()
