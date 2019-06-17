# app/history/views.py

from flask import render_template, jsonify, request
from flask_login import login_required, current_user

from . import history
from ..models import Expense, Budget
from .. import db
from ..app_processes import getYearToDateSavings, getMonthSavings, getYearSavings, getDaySavings, getDateRangeSavings
from datetime import datetime, date
from calendar import month_name


@history.route('/history')
@login_required
def historyPage():
    """
    Render the history template
    """

    today = datetime.now().date()
    budget = Budget.query.filter(Budget.user_id == current_user.id).first()
    ytd_savings = getYearToDateSavings(budget, current_user.id)
    month_savings = getMonthSavings(today.month, today.year, today, budget, current_user.id)
    today_savings = getDaySavings(today, budget, current_user.id)
    minDate = budget.creation_date

    return render_template('history/history.html', ytdSavings=ytd_savings,
                                                    monthSavings=month_savings,
                                                    todaySavings=today_savings,
                                                    todayYear=today.year,
                                                    todayMonth=month_name[today.month],
                                                    todayDate=today.strftime("%B %d, %Y"),
                                                    minDate=minDate)


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

    month_savings = getMonthSavings(month, year, todayDate, budget, current_user.id)

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
    day_savings = getDaySavings(selectedDate, budget, current_user.id)

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
    year_savings = getYearSavings(year, budget, current_user.id)

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

    day_savings = getDateRangeSavings(selectedDate1, selectedDate2, budget, current_user.id)

    resp = jsonify(status_code=200,
                    savings = day_savings)
    return resp
