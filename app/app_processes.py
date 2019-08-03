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


def getDateExpenses(date, id):
    """
    Params:
        date: A Date object.
        id: user ID.
    Returns list of expenses for given date.
    """

    expenses = Expense.query.filter(Expense.date==date, Expense.user_id==id).order_by(Expense.id.desc()).all()

    return expenses


def getDateTotalExpense(date, id):

    expenses = Expense.query.with_entities(func.sum(Expense.cost)).filter(Expense.date==date, Expense.user_id==id).scalar()

    return roundCost(expenses)


def getMonthTotalExpenses(month, year, id):

    numDaysInMonth = monthrange(year, month)[1]
    firstDate = date(year, month, 1)
    lastDate = date(year, month, numDaysInMonth)

    expenses = Expense.query.with_entities(func.sum(Expense.cost)).filter(Expense.date>=firstDate, Expense.date<=lastDate, Expense.user_id==id).scalar()

    return roundCost(expenses)


def getYearTotalExpenses(year, id):

    # January 1 of selected year
    firstDayOfYear = date(year, 1, 1)

    # December 31 of selected year
    lastDayOfYear = date(year, 12, 31)

    expenses = Expense.query.with_entities(func.sum(Expense.cost)).filter(Expense.date>=firstDayOfYear, Expense.date<=lastDayOfYear, Expense.user_id==id).scalar()

    return roundCost(expenses)


def getDateRangeTotalExpenses(date1, date2, id):

    timeDiff = date2 - date1
    numDays = timeDiff.days + 1

    expenses = Expense.query.with_entities(func.sum(Expense.cost)).filter(Expense.user_id==id, Expense.date>=date1, Expense.date<=date2).scalar()

    return roundCost(expenses)


def getChartExpenseDataForDate(date, id):
    """
    Returns array of arrays for each category and total percentage of costs for each category; ex.: [['Food', 25], ...] == 25% of expenses were spent on food
    """
    expenses = Expense.query.with_entities(Expense.category, Expense.cost).filter(Expense.user_id==id, Expense.date==date).all()

    expenses = sumCategoryData(expenses)
    expenses = convertToChartData(expenses)
    return expenses


def getChartExpenseDataForDateRange(date1, date2, id):
    """
    date1: Start date
    date2: End date
    Returns array of arrays for each category and total percentage of costs for each category; ex.: [['Food', 25], ...] == 25% of expenses were spent on food
    """

    expenses = Expense.query.with_entities(Expense.category, Expense.cost).filter(Expense.user_id==id, Expense.date>=date1, Expense.date<=date2).all()

    expenses = sumCategoryData(expenses)
    expenses = convertToChartData(expenses)
    return expenses


def getChartExpenseDataForMonth(month, year, id):
    """
    Returns array of arrays for each category and total percentage of costs for each category; ex.: [['Food', 25], ...] == 25% of expenses were spent on food
    """
    numDaysInMonth = monthrange(year, month)[1]
    firstDate = date(year, month, 1)
    lastDate = date(year, month, numDaysInMonth)

    expenses = Expense.query.with_entities(Expense.category, Expense.cost).filter(Expense.date>=firstDate, Expense.date<=lastDate, Expense.user_id==id).all()

    expenses = sumCategoryData(expenses)
    expenses = convertToChartData(expenses)
    return expenses


def getChartExpenseDataForYear(year, id):
    """
    Returns array of arrays for each category and total percentage of costs for each category; ex.: [['Food', 25], ...] == 25% of expenses were spent on food
    """

    # January 1 of selected year
    firstDayOfYear = date(year, 1, 1)

    # December 31 of selected year
    lastDayOfYear = date(year, 12, 31)

    expenses = Expense.query.with_entities(Expense.category, Expense.cost).filter(Expense.date>=firstDayOfYear, Expense.date<=lastDayOfYear, Expense.user_id==id).all()

    expenses = sumCategoryData(expenses)
    expenses = convertToChartData(expenses)
    return expenses


def sumCategoryData(expenseArrOfTups):
    """
    expenseArrOfTups: Array of tuples like (category, cost)
    Returns a dictionary with entries as category and value as total cost; ex.: {'Food': 500, 'Entertainment': 300, ...}
    """

    categoryDic = getExpenseCategories()

    for expense in expenseArrOfTups:
        categoryDic[expense[0]] += expense[1]

    return categoryDic


def convertToChartData(categoryDic):
    """
    categoryDic: Dictionary like {'Food': 500, 'Entertainment': 300, ...}
    Returns an array of arrays each have a category and percentage of all expenses like [['Food', 25], ['Entertainment': 15], ...]
    """

    total = 0
    for category in categoryDic:
        total += categoryDic[category]

    chartDataArr = []
    for category in getExpenseCategoriesOrder():
        if not total:
            chartDataArr.append([category, 0])
        else:
            chartDataArr.append([category, round((categoryDic[category] / total * 100), 2)])

    return chartDataArr


# def getChartData(expensesArr):
#     """
#     expenseArr: Array of expense objects
#     Returns array of arrays for each category and sum of expenses for category
#     """
#
#     sumCategoryData(expenseArr)



######################### Helper functions ############################

def roundCost(cost):
    """
    Return the cost rounded to 2 decimal places
    """

    if cost:
        return round(cost * 100) / 100
    else:
        return 0


def getExpenseCategories():
    """
    Return an dictionary with entries as categories and values set to 0
    """
    """
    Note that any changes to the categories here, will require same changes to be done in app/home/form.py ExpenseForm.category field
    and getExpenseCategoriesOrder().
    """

    return {"Food": 0,
            "Entertainment": 0,
            "Health": 0,
            "Debt": 0,
            "Gift": 0,
            "Education": 0,
            "Travel": 0,
            "Other": 0}


def getExpenseCategoriesOrder():
    """
    Returns array of Categories
    """

    return ['Food',
            "Entertainment",
            "Health",
            "Debt",
            "Gift",
            "Education",
            "Travel",
            "Other"]
