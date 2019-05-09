# app/home/views.py

from flask import render_template, jsonify
from flask_login import login_required, current_user

from . import home
from ..models import Expense, Budget
from forms import ExpenseForm, BudgetForm
from .. import db
from ..app_processes import getTodayBudgetRemaining,
                            getWeekBudgetRemaining
                            getMonthBudgetRemaining,
                            getWeekBudgetRemaining

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
    today_expenses = Expense.query.filter_by(date=todayDate, user_id=current_user.id).order_by(Expense.id.desc()).all()

    # get budget
    budget = Budget.query.filter_by(user_id=current_user.id).first()

    ## calculate year-to-date savings
    savings = 0
    if budget:
        num_of_days_ytd = todayDate - budget.creation_date
        ytd_budget = num_of_days_ytd * budget.daily
        ytd_expense_cost = Expense.query.with_entities(func.sum(Expense.cost).label('total')).filter_by(id=current_user.id).filter(and_(Expense.date >= budget_creation_date, Expense.date <= todayDate)).scalar()
        if ytd_expense_cost:
            savings = ytd_budget - ytd_expenses.total


    # add expense form
    expense_form = ExpenseForm()

    return render_template('home/dashboard.html', title="Dashboard", today_expenses=today_expenses, budget=budget, savings=savings, expense_form=expense_form)


@home.route('/add-expense', methods=['POST'])
@login_required
def addExpense():
    """
    Add an expense to the expense list
    """

    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(item=form.item.data,
                          cost=form.cost.data,
                          category=form.category.data,
                          date=datetime.now().date(),
                          user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()

        resp = jsonify(success=True, item=form.item.data, cost=float(form.cost.data))
        resp.status_code = 201
    else:
        resp = jsonify(success=False, errors=form.errors)

    return resp


@home.route('/edit-budget', methods=['POST'])
@login_required
def editBudget():
    """
    Edit budgets
    """

    form = BudgetForm()
    if form.validate_on_submit():
        budget = Budget.query.filter_by(user_id=current_user.id).first()
        budget.daily = form.daily
        budget.weekly = form.weekly
        budget.monthly = form.monthly
        budget.yearly = form.yearly
        db.session.add(budget)
        db.session.commit()

        # get the remaining budgets
        todayBudgetRemain = getTodayBudgetRemaining(budget, current_user.id)
        weekBudgetRemain = getWeekBudgetRemaining(budget, current_user.id)
        monthBudgetRemain = getMonthBudgetRemaining(budget, current_user.id)
        yearBudgetRemain = getYearBudgetRemaining(budget, current_user.id)

        resp = jsonify(success=True,
                       today=todayBudgetRemain,
                       week=getWeekBudgetRemaining,
                       month=getMonthBudgetRemaining,
                       year=getYearBudgetRemaining)
    else:
        resp = jsonify(sucess=False)

    return resp
