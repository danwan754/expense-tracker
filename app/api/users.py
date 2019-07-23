# app/api/users.py

from datetime import datetime, date
from re import match

from flask import url_for, jsonify, request
from flask_login import login_required, current_user

from .. import db
from app.api import bp
from ..models import Expense, Budget
from ..home.forms import ExpenseForm, BudgetForm
from ..app_processes import getDateExpenses


@bp.route('/users/expenses', methods=['POST'])
@login_required
def create_expense():
    """
    Create a new expense
    """

    form = ExpenseForm(request.form)
    if form.validate_on_submit():
        expense = Expense(item=form.item.data,
                          cost=form.cost.data,
                          category=form.category.data,
                          date=form.date.data,
                          user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()

        # resp = jsonify(success=True, item=form.item.data, cost=float(form.cost.data))
        resp = jsonify(expense.to_dict())
        resp.status_code = 201
        resp.headers['Location'] = url_for('api.get_expense', user_id=id, expense_id=expense.id)
    else:
        resp = jsonify(errors=form.errors)
        resp.status_code = 400

    return resp


@bp.route('/users/expenses', methods=['PUT'])
@login_required
def update_expense():
    """
    Update a current expense
    """

    print("#####")
    print(request.form)
    form = ExpenseForm(request.form)
    if form.validate():

        expense_id = request.args['id']

        # get the expense to update
        expense = Expense.query.get(expense_id)

        expense.item = form.item.data
        expense.cost = form.cost.data
        expense.category = form.category.data
        db.session.commit()

        resp = jsonify(expense.to_dict())
        resp.status_code = 200
        resp.headers['Location'] = url_for('api.get_expense', user_id=id, expense_id=expense.id)
    else:
        resp = jsonify(errors=form.errors)
        resp.status_code = 400

    return resp


@bp.route('/users/expenses', methods=['GET'])
def get_expenses():
    """ get expenses on the provided date"""

    date = request.args['date']

    expenses = getDateExpenses(date, current_user.id)

    return jsonify(expenses.to_collection())




@bp.route('/users/expenses', methods=['GET'])
def get_expense():
    """ get an expense"""

    return jsonify(Expense.query.get_or_404(expense_id).to_dict())



@bp.route('/users/expenses', methods=['DELETE'])
def delete_expense():
    """
    Delete expense with the provided item name, cost, and date
    """

    data = request.get_json()
    id = data['id']

    expense = Expense.query.filter(Expense.user_id==current_user.id, Expense.id==id).first()

    if expense:
        db.session.delete(expense)
        db.session.commit()

    resp = jsonify(success=True)
    resp.status_code = 204
    return resp




@bp.route('/users/budget', methods=['GET'])
def get_budget():
    pass
