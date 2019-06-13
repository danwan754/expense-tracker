# app/history/views.py

from flask import render_template, jsonify, request
from flask_login import login_required, current_user

from . import history
from ..models import Expense, Budget
from .. import db
from ..app_processes import getSavings


@history.route('/history')
@login_required
def historyPage():
    """
    Render the history template
    """

    budget = Budget.query.filter(Budget.user_id == current_user.id).first()
    ytd_savings = getSavings(budget, current_user.id)

    return render_template('history/history.html', ytd_savings=ytd_savings)


@history.route('/month-savings', methods=['GET'])
@login_required
def totalSavings():
    """
    Get the savings for this month
    """

    budget = Budget.query.filter(Budget.user_id == current_user.id).first()

    year = request.data.year
    month = request.data.month

    month_savings = getMonthSavings(year, month, budget, current_user.id)

    resp = jsonify(status_code=200,
                    savings = month_savings)

    return resp
