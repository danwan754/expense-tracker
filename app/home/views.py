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

    todayDate = datetime.now().date();
    today_expenses = Expense.query.filter_by(date=todayDate).all()

    # if today_expenses:
    #     print("THERE ARE EXPENSESSSSSSSSSS")
    #     print(today_expenses)
    # else:
    #     print("NO EXPENSESSSSS")

    budgets = Budget.query.filter_by(id=current_user.budget_id).first()

    return render_template('home/dashboard.html', title="Dashboard", today_expenses=today_expenses, budgets=budgets)
