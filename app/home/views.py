# app/home/views.py

from flask import render_template
from flask_login import login_required, current_user

from . import home
from ..models import Expense, Budget

from datetime import datetime

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """

    # get today's expenses
    todayDate = datetime.now().date();
    today_expenses = Expense.query.filter_by(date=todayDate).all()

    # get budget
    budget = Budget.query.filter_by(id=current_user.budget_id).first()

    ## calculate year-to-date savings
    savings = 0
    if budget:
        num_of_days_ytd = todayDate - budget.creation_date
        ytd_budget = num_of_days_ytd * budget.daily
        ytd_expense_cost = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(id=current_user.id).filter(and_(Expense.date >= budget_creation_date, Expense.date <= todayDate)).scalar()
        if ytd_expense_cost:
            savings = ytd_budget - ytd_expenses.total

    return render_template('home/dashboard.html', title="Dashboard", today_expenses=today_expenses, budget=budget, savings=savings)
