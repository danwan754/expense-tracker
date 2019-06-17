# app/history/views.py

from flask import render_template, jsonify, request
from flask_login import login_required, current_user

from . import history
from ..models import Expense, Budget
from .. import db
from ..app_processes import getYearToDateSavings, getMonthSavings, getYearSavings, getDaySavings
from datetime import datetime


@history.route('/history')
@login_required
def historyPage():
    """
    Render the history template
    """

    budget = Budget.query.filter(Budget.user_id == current_user.id).first()
    ytd_savings = getYearToDateSavings(budget, current_user.id)
    minDate = budget.creation_date

    return render_template('history/history.html', savings=ytd_savings, minDate=minDate)


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
    date = date(request.args['year'], request.args['month'], request.args['day'])
    day_savings = getDaySavings(date, budget, current_user.id)

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
