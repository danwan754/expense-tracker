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
    else:
        todayExpenses = roundCost(todayExpenses)

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
    else:
        weekExpenses = roundCost(weekExpenses)

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

    totalMonthExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter(Expense.user_id == id, Expense.date >= firstDateOfMonth, Expense.date <= todayDate).scalar()

    if not totalMonthExpenses:
        totalMonthExpenses = 0
    else:
        totalMonthExpenses = roundCost(totalMonthExpenses)

    # if budget created this month, then this month's budget starts from
    # day of budget creation to end of month
    if budget.creation_date.month == todayMonth:
        timeDiff = lastDateOfMonth - budget.creation_date
        numDays = timeDiff.days

    monthBudget = budget.daily * numDays

    monthBudgetRemain = monthBudget - totalMonthExpenses

    return monthBudgetRemain


# def getYearBudgetRemaining(budget, id):
#
#     """
#     Param:
#         budget: A Budget object.
#         id: user ID.
#     Returns the remaining budget for the current year.
#     """
#
#     todayDate = datetime.now().date()
#     todayYear = todayDate.year()
#     numDaysInYear = 365
#
#     budgetCreationDate = Budget.query.with_entities(Budget.creation_date).filter(Budget.user_id=id).first()
#     endOfYearDate = date(todayYear, 12, 31)
#
#     totalYearExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(user_id=id).filter(Expense.date >= budgetCreationDate, Expense.date <= endOfYearDate).scalar()
#
#     if not totalYearExpenses:
#         totalYearExpenses = 0
#
#     if (isleap(todayYear)):
#         numDaysInYear = 366
#
#     yearBudget = budget.daily * numDaysInYear
#
#     yearBudgetRemain = yearBudget - totalYearExpenses
#
#     return yearBudgetRemain


def getAllBudgetsRemaining(budget, id):

    """
    Param:
        budget: A Budget object.
        id: user ID.
    Returns the remaining budgets in dictionary like: {'today': [value], 'week': [value], 'month': [value]}
    """

    # get the remaining budgets
    todayBudgetRemain = getTodayBudgetRemaining(budget, id)
    weekBudgetRemain = getWeekBudgetRemaining(budget, id)
    monthBudgetRemain = getMonthBudgetRemaining(budget, id)
    # yearBudgetRemain = getYearBudgetRemaining(budget, id)

    allBudgetsRemain = {'today': todayBudgetRemain,
                        'week': weekBudgetRemain,
                        'month': monthBudgetRemain
                        # 'year': yearBudgetRemain
                        }

    return allBudgetsRemain


def getSavings(budget, id):
    """
    Params:
        budget: A Budget object.
        id: user ID.
    Returns the total savings to date. Note that value can be negative due to
    going over budget.
    """

    totalExpenses = Expense.query.filter(Expense.user_id == id).with_entities(func.sum(Expense.cost).label('total')).scalar()

    if totalExpenses:
        totalExpenses = roundCost(totalExpenses)
    else:
        totalExpenses = 0


    todayDate = datetime.now().date()
    timeDiff = todayDate - budget.creation_date
    numDays = timeDiff.days

    # total budget since budget creation date
    totalBudget = budget.daily * numDays

    savings = totalBudget - totalExpenses

    return savings


def roundCost(cost):
    """
    Return the cost rounded to 2 decimal places
    """

    return round(cost * 100) / 100
