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


def getYearToDateSavings(budget, id):
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


def getMonthSavings(month, year, todayDate, budget, id):
    """
    Params:
        month: Month as a number where 1 = January, 12 = December
        year: Year as a number. Ex.: 2019
        budget: A Budget object.
        id: user ID.
    Returns the total savings for month of year.
    """

    numDaysInMonth = monthrange(year, month)[1]
    firstDate = date(year, month, 1)
    lastDate = date(year, month, numDaysInMonth)

    # if budget created in same month and year, calculate partial month budget starting from from budget creation date
    if budget.creation_date.month == month and budget.creation_date.year == year:

        # if budget created on same month and year as today, calculate partial month budget from creation date to today
        if todayDate.month == budget.creation_date.month and todayDate.year == budget.creation_date.year:
            timeDiff = todayDate - budget.creation_date

        else:
            timeDiff = lastDate - budget.creation_date

        # include the budget creation day
        numDays = timeDiff.days + 1

    else:
        numDays = numDaysInMonth

    monthBudget = budget.daily * numDays

    expenses = Expense.query.filter(Expense.user_id == id, Expense.date <= lastDate, Expense.date >= firstDate).with_entities(func.sum(Expense.cost).label('total')).scalar()

    if expenses:
        expenses = roundCost(expenses)
    else:
        expenses = 0

    savings = monthBudget - expenses

    return savings


def getDaySavings(date, budget, id):
    """
    Params:
        date: A Date object.
        budget: A Budget object.
        id: user ID.
    Returns the total savings for date.
    """

    dailyBudget = budget.daily

    expenses = Expense.query.filter(Expense.user_id==id, Expense.date==date).with_entities(func.sum(Expense.cost).label('total')).scalar()

    if expenses:
        expenses = roundCost(expenses)
    else:
        expenses = 0

    savings = dailyBudget - expenses

    return savings


def getYearSavings(year, budget, id):
    """
    Params:
        year: integer.
        budget: A Budget object.
        id: user ID.
    Returns the total savings for year in date.
    """

    creationYear = budget.creation_date.year

    # if the selected year is during year that budget was created, get savings for that year where starting day is budget creation date
    if creationYear == year:
        return getYearToDateSavings(budget, id)

    # January 1 of selected year
    firstDayOfYear = date(year, 1, 1)

    # December 31 of selected year
    lastDayOfYear = date(year, 12, 31)

    numDaysInYear = 365

    expenses = Expense.query.filter(Expense.user_id==id, Expense.date>=firstDayOfYear, Expense.date<=lastDayOfYear).with_entities(func.sum(Expense.cost).label('total')).scalar()

    if expenses:
        expenses = roundCost(expenses)
    else:
        expenses = 0

    if (isleap(year)):
        numDaysInYear = 366

    yearBudget = budget.daily * numDaysInYear

    savings = yearBudget - expenses

    return savings


def getDateRangeSavings(date1, date2, budget, id):
    """
    Params:
        date1: A Date object for a starting date.
        date2: A Date object for an ending date.
        budget: A Budget object.
        id: user ID.
    Returns the total savings for a date range.
    """

    timeDiff = date2 - date1
    numDays = timeDiff.days + 1

    expenses = Expense.query.filter(Expense.user_id==id, Expense.date>=date1, Expense.date<=date2).with_entities(func.sum(Expense.cost).label('total')).scalar()

    if expenses:
        expenses = roundCost(expenses)
    else:
        expenses = 0

    dateRangeBudget = budget.daily * numDays

    savings = dateRangeBudget - expenses

    return savings


def roundCost(cost):
    """
    Return the cost rounded to 2 decimal places
    """

    return round(cost * 100) / 100
