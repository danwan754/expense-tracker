# app/history/views.py

from flask import render_template, jsonify, request
from flask_login import login_required, current_user

from . import history
from ..models import Expense, Budget
from ..home.forms import ExpenseForm
from .. import db
from ..app_processes import getYearToDateSavings, getMonthSavings, getYearSavings, getDaySavings, getDateRangeSavings, getDateTotalExpense, getMonthTotalExpenses, getYearTotalExpenses, getDateRangeTotalExpenses, getChartExpenseDataForDate, getChartExpenseDataForDateRange, getChartExpenseDataForMonth, getChartExpenseDataForYear
from datetime import datetime, date
from calendar import month_name


@history.route('/history')
@login_required
def historyPage():
    """
    Render the history template
    """

    today = datetime.now().date()
    expenseForm = ExpenseForm()
    budget = Budget.query.filter(Budget.user_id == current_user.id).first()

    if budget:
        ytd_savings = getYearToDateSavings(budget, current_user.id)
        month_savings = getMonthSavings(today.month, today.year, today, budget, current_user.id)
        today_savings = getDaySavings(today, budget, current_user.id)
        minDate = budget.creation_date

        # add a comma for each thousands
        ytd_savings = "{:,}".format(ytd_savings)
        month_savings = "{:,}".format(month_savings)
        today_savings = "{:,}".format(today_savings)
    else:
        ytd_savings = 0
        month_savings = 0
        today_savings = 0
        minDate = today.strftime("%B %d, %Y")

    return render_template('history/history.html', ytdSavings=ytd_savings,
                                                    monthSavings=month_savings,
                                                    todaySavings=today_savings,
                                                    todayYear=today.year,
                                                    todayMonth=month_name[today.month],
                                                    todayDate=today.strftime("%B %d, %Y"),
                                                    minDate=minDate,
                                                    expenseForm=expenseForm)


@history.route('/month-savings', methods=['GET'])
@login_required
def monthSavings():
    """
    Get the savings for this month
    """

    budget = Budget.query.filter(Budget.user_id == current_user.id).first()
    month = int(request.args['month'])
    year = int(request.args['year'])
    todayDate = datetime.now().date()

    if budget:
        month_savings = getMonthSavings(month, year, todayDate, budget, current_user.id)
    else:
        month_savings = 0

    resp = jsonify(status_code=200,
                    savings = month_savings)

    return resp


@history.route('/day-savings', methods=['GET'])
@login_required
def daySavings():
    """
    Get the savings for date
    """

    budget = Budget.query.filter(Budget.user_id == current_user.id).first()
    year = int(request.args['year'])
    month = int(request.args['month'])
    day = int(request.args['day'])
    selectedDate = date(year, month, day)

    if budget:
        day_savings = getDaySavings(selectedDate, budget, current_user.id)
    else:
        day_savings = 0

    resp = jsonify(status_code=200,
                    savings = day_savings)
    return resp


@history.route('/year-savings', methods=['GET'])
@login_required
def yearSavings():
    """
    Get the savings for year
    """

    budget = Budget.query.filter(Budget.user_id == current_user.id).first()
    year = int(request.args['year'])

    if budget:
        year_savings = getYearSavings(year, budget, current_user.id)
    else:
        year_savings = 0

    resp = jsonify(status_code=200,
                    savings = year_savings)
    return resp


@history.route('/date-range-savings', methods=['GET'])
@login_required
def dateRangeSavings():
    """
    Get the savings for date range
    """

    budget = Budget.query.filter(Budget.user_id == current_user.id).first()
    year1 = int(request.args['year1'])
    month1 = int(request.args['month1'])
    day1 = int(request.args['day1'])
    year2 = int(request.args['year2'])
    month2 = int(request.args['month2'])
    day2 = int(request.args['day2'])
    selectedDate1 = date(year1, month1, day1)
    selectedDate2 = date(year2, month2, day2)


    if budget:
        day_savings = getDateRangeSavings(selectedDate1, selectedDate2, budget, current_user.id)
    else:
        day_savings = 0

    resp = jsonify(status_code=200,
                    savings = day_savings)
    return resp


@history.route('/day-expenses', methods=['GET'])
@login_required
def dayExpenses():
    """
    Get total expenses for date
    """

    year = int(request.args['year'])
    month = int(request.args['month'])
    day = int(request.args['day'])
    selectedDate = date(year, month, day)

    day_expenses = getDateTotalExpense(selectedDate, current_user.id)

    resp = jsonify(status_code=200,
                    savings = day_expenses)
    return resp


@history.route('/month-expenses', methods=['GET'])
@login_required
def monthExpenses():
    """
    Get the total expenses for month
    """

    month = int(request.args['month'])
    year = int(request.args['year'])

    month_expenses = getMonthTotalExpenses(month, year, current_user.id)

    resp = jsonify(status_code=200,
                    savings = month_expenses)
    return resp


@history.route('/year-expenses', methods=['GET'])
@login_required
def yearExpenses():
    """
    Get the total expenses for year
    """

    year = int(request.args['year'])
    year_expenses = getYearTotalExpenses(year, current_user.id)

    resp = jsonify(status_code=200,
                    savings = year_expenses)
    return resp


@history.route('/date-range-expenses', methods=['GET'])
@login_required
def dateRangeExpenses():
    """
    Get the total expenses for date range
    """

    year1 = int(request.args['year1'])
    month1 = int(request.args['month1'])
    day1 = int(request.args['day1'])
    year2 = int(request.args['year2'])
    month2 = int(request.args['month2'])
    day2 = int(request.args['day2'])
    selectedDate1 = date(year1, month1, day1)
    selectedDate2 = date(year2, month2, day2)

    date_range_expenses = getDateRangeTotalExpenses(selectedDate1, selectedDate2, current_user.id)

    resp = jsonify(status_code=200,
                    savings = date_range_expenses)
    return resp


@history.route('/day-expense-chart', methods=['GET'])
@login_required
def dayExpenseChart():
    """
    Get expenditure stats for date
    """

    date = datetime.strptime(request.args['date'], "%Y-%m-%d").date()

    chart_data = getChartExpenseDataForDate(date, current_user.id)

    resp = jsonify(status_code=200,
                    chartData = chart_data)
    return resp


@history.route('/date-range-chart', methods=['GET'])
@login_required
def dateRangeChart():
    """
    Get expenditure stats for date range
    """

    start = datetime.strptime(request.args['start'], "%Y-%m-%d").date()
    end = datetime.strptime(request.args['end'], "%Y-%m-%d").date()
    chart_data = getChartExpenseDataForDateRange(start, end, current_user.id)

    resp = jsonify(status_code=200,
                    chartData = chart_data)
    return resp


@history.route('/month-chart', methods=['GET'])
@login_required
def monthExpenseChart():
    """
    Get expenditure stats for month
    """

    month = int(request.args['month'])
    year = int(request.args['year'])

    # day_expenses_objs = getDateExpenses(date, current_user.id)
    chart_data = getChartExpenseDataForMonth(month, year, current_user.id)

    resp = jsonify(status_code=200,
                    chartData = chart_data)
    return resp


@history.route('/year-chart', methods=['GET'])
@login_required
def yearExpenseChart():
    """
    Get expenditure stats for year
    """

    year = int(request.args['year'])

    # day_expenses_objs = getDateExpenses(date, current_user.id)
    chart_data = getChartExpenseDataForYear(year, current_user.id)

    resp = jsonify(status_code=200,
                    chartData = chart_data)
    return resp
