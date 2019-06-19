# app/api/expenses.py

from app.api import expenses




@expenses.route('/expenses', methods=['GET'])
def create_expense():
    pass


@expenses.route('/expenses', methods=['POST'])
def get_expenses():
    pass


@expenses.route('/expenses/<int:id>', methods=['GET'])
def get_expense():
    pass


@expenses.route('/expenses/<int:id>', methods=['PUT'])
def update_expense():
    pass


@expenses.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense():
    pass
