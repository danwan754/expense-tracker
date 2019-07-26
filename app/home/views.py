# app/home/views.py

from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy.sql import func

from . import home
from ..models import Expense, Budget
from forms import ExpenseForm, BudgetForm
from .. import db
from ..app_processes import getAllBudgetsRemaining, getYearToDateSavings, getDateExpenses

from datetime import datetime, date, timedelta

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
    todayDate = date.today()
    today_expenses = getDateExpenses(todayDate, current_user.id)

    # get budget
    budget = Budget.query.filter_by(user_id=current_user.id).first()

    budgetsRemaining = None
    savings = None

    if budget:
        # get the remaining budgets for today, this week, this month
        budgetsRemaining = getAllBudgetsRemaining(budget, current_user.id)

        # get total savings since budget creation
        savings = getYearToDateSavings(budget, current_user.id)

    expenseForm = ExpenseForm()
    budgetForm = BudgetForm()

    return render_template('home/dashboard.html', title="Dashboard", today_expenses=today_expenses, budget=budgetsRemaining, savings=savings, expenseForm=expenseForm, budgetForm=budgetForm)


# @home.route('/add-expense', methods=['POST'])
# @login_required
# def addExpense():
#     """
#     Add an expense for today.
#     """
#
#     form = ExpenseForm(request.form)
#     if form.validate_on_submit():
#         expense = Expense(item=form.item.data,
#                           cost=form.cost.data,
#                           category=form.category.data,
#                           date=date.today(),
#                           user_id=current_user.id)
#         db.session.add(expense)
#         db.session.commit()
#
#         resp = jsonify(success=True, item=form.item.data, cost=float(form.cost.data))
#         resp.status_code = 201
#     else:
#         resp = jsonify(success=False, errors=form.errors)
#
#     return resp


@home.route('/edit-budget', methods=['POST'])
@login_required
def editBudget():
    """
    Edit budgets and return the recalculated remaining budgets.
    """

    form = BudgetForm(request.form)
    # if form.validate_on_submit():
    if request.method == 'POST' and form.validate():
        budget = Budget.query.filter_by(user_id=current_user.id).first()

        if not budget:
            budget = Budget(user_id=current_user.id)
            budget.creation_date = date.today()

        budget.daily = form.data["dailyBudgetField"]
        # budget.weekly = form.data["weeklyBudgetField"]
        # budget.monthly = form.data["monthlyBudgetField"]
        # budget.yearly = form.data["yearlyBudgetField"]
        db.session.add(budget)
        db.session.commit()

        # get the remaining budgets
        budgetsRemaining = getAllBudgetsRemaining(budget, current_user.id)

        resp = jsonify(success=True,
                       budget=budgetsRemaining)
    else:
        resp = jsonify(sucess=False,
                        errors=form.errors)

    return resp






@home.route('/test')
def test():
    """
    Just some testing anything to see json response on browser.
    """

    budget = Budget.query.filter_by(user_id=current_user.id).first()
    budgetsRemaining = getAllBudgetsRemaining(budget, current_user.id)
    resp = jsonify(success=True,
                    budget=budgetsRemaining)
    return resp
