from ..models import Expense, Budget
from .. import db

from datetime import datetime
from calendar import monthrange, isLeap


def getTodayBudgetRemaining(budget, id):

    """
    Params:
        budget: A Budget object.
        id: user ID.
    Returns the remaining budget for today.
    """

    todayDate = datetime.now().date

    todayExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter(_and(user_id=id, Expense.date == todayDate)).scalar()

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

    todayDate = datetime.now().date

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
        startDate = datetime.now().date - datetime.timedelta(days=numDays)
    else:
        numDays = 7 - (startWeekDay - todayWeekDay)
        startDate = datetime.now().date - datetime.timedelta(days=numDays)

    # this week's expenses
    weekExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(user_id=id).filter(_and(Expense.date >= startDate, Expense.date <= todayDate)).scalar()

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

    todayDate = datetime.now().date
    todayMonth = todayDate.month()
    todayYear = todayDate.year()

    totalMonthExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(user_id=id).filter(Expense.date.month()=todayMonth).scalar()

    # number of days in this month
    numDays = monthrange(todayYear, todayMonth)

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

    todayDate = datetime.now().date
    todayYear = todayDate.year()
    numDaysInYear = 365

    totalYearExpenses = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(user_id=id).filter(_and(Expense.date.year() = todayYear))

    if (isLeap(todayYear)):
        numDaysInYear = 366

    yearBudget = budget.daily * numDaysInYear

    yearBudgetRemain = yearBudget - totalYearExpenses

    return yearBudgetRemain


    
# # sum of expenses for each day
# dailyExpensesList = Expense.query.with_entities(Expense.date, func.sum(Expense.cost)).group_by(Expense.date).order_by(Expense.date.desc()).all()

# for expenseTuple in dailyExpensesList:
