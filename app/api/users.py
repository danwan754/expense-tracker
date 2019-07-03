# app/api/users.py

from datetime import datetime, date
from re import match

from flask import url_for, jsonify, request
from flask_login import login_required, current_user

from .. import db
from app.api import bp
from ..models import Expense, Budget
from ..home.forms import ExpenseForm, BudgetForm



@bp.route('/users/expenses', methods=['POST'])
@login_required
def create_expense():

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


@bp.route('/users/expenses', methods=['GET'])
def get_expenses():
    """ get date from arguments"""
    pass


@bp.route('/users/expenses', methods=['GET'])
def get_expense():
    """ get expenses for a date"""
    return jsonify(Expense.query.get_or_404(expense_id).to_dict())


@bp.route('/users/expenses', methods=['PUT'])
def update_expense(id):
    pass


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







@bp.route('/users/<int:id>/budget', methods=['GET'])
def get_budget(id):
    pass
