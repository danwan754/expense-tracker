from models import Expense, Budget
from . import db

from datetime import datetime, timedelta, date
from calendar import monthrange, isleap
from sqlalchemy.sql import func



def getTodayBudgetRemaining(budget, id):

    """
    Params:
        budget: A Budget object.
        id: user ID.
    Returns the remaining budget for today.
    """

    todayDate = datetime.now().date()

    todayExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter(Expense.user_id==id, Expense.date==todayDate).scalar()

    if not todayExpenses:
        todayExpenses = 0

    # remaining budget for today
    todayBudgetRemain = budget.daily - todayExpenses

    return todayBudgetRemain


def getWeekBudgetRemaining(budget, id):

    """
    Param:
        budget: A Budget object.
        id: user ID.
    Returns the remaining budget for the current week.
    """

    todayDate = datetime.now().date()

    # today's weekday as an integer where Monday = 0, Sunday = 6
    todayWeekDay = todayDate.weekday()

    # weekday of the starting day of week as the budget creation day
    startWeekDay = budget.creation_date.weekday()

    # number of days that today is ahead of start day
    numDays = 0

    if todayWeekDay == startWeekDay:
        startDate = todayDate
    elif todayWeekDay > startWeekDay:
        numDays = todayWeekDay - startWeekDay
        startDate = datetime.now().date() - timedelta(days=numDays)
    else:
        numDays = 7 - (startWeekDay - todayWeekDay)
        startDate = datetime.now().date() - timedelta(days=numDays)

    # this week's expenses
    weekExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(user_id=id).filter(Expense.date >= startDate, Expense.date <= todayDate).scalar()

    if not weekExpenses:
        weekExpenses = 0

    # remaining weekly budget
    weekBudgetRemain = (budget.daily * 7) - weekExpenses

    return weekBudgetRemain


def getMonthBudgetRemaining(budget, id):

    """
    Param:
        budget: A Budget Object.
        id: user ID.
    Returns the remaining budget for the current month.
    """

    todayDate = datetime.now().date()
    todayMonth = todayDate.month
    todayYear = todayDate.year

    # number of days in this month
    numDays = monthrange(todayYear, todayMonth)[1]

    firstDateOfMonth = date(todayYear, todayMonth, 1)
    lastDateOfMonth = date(todayYear, todayMonth, numDays)

    totalMonthExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(user_id=id).filter(Expense.date >= firstDateOfMonth, Expense.date <= lastDateOfMonth).scalar()

    if not totalMonthExpenses:
        totalMonthExpenses = 0


    monthBudget = budget.daily * numDays

    monthBudgetRemain = monthBudget - totalMonthExpenses

    return monthBudgetRemain


def getYearBudgetRemaining(budget, id):

    """
    Param:
        budget: A Budget object.
        id: user ID.
    Returns the remaining budget for the current year.
    """

    todayDate = datetime.now().date()
    todayYear = todayDate.year()
    numDaysInYear = 365

    totalYearExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(user_id=id).filter(Expense.date.year()==todayYear).scalar()

    if (isleap(todayYear)):
        numDaysInYear = 366

    yearBudget = budget.daily * numDaysInYear

    yearBudgetRemain = yearBudget - totalYearExpenses

    return yearBudgetRemain


def getAllBudgetsRemaining(budget, id):

    """
    Param:
        budget: A Budget object.
        id: user ID.
    Returns the remaining budgets in dictionary like: {'today': [value], 'week': [value], 'month': [value], 'year': [value]}
    """

    # get the remaining budgets
    todayBudgetRemain = getTodayBudgetRemaining(budget, id)
    weekBudgetRemain = getWeekBudgetRemaining(budget, id)
    monthBudgetRemain = getMonthBudgetRemaining(budget, id)
    yearBudgetRemain = getYearBudgetRemaining(budget, id)

    allBudgetsRemain = {'today': todayBudgetRemain,
                        'week': weekBudgetRemain,
                        'month': monthBudgetRemain,
                        'year': yearBudgetRemain}

    return allBudgetsRemain



# # sum of expenses for each day
# dailyExpensesList = Expense.query.with_entities(Expense.date, func.sum(Expense.cost)).group_by(Expense.date).order_by(Expense.date.desc()).all()

# for expenseTuple in dailyExpensesList:
