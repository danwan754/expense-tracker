# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired

# from ..models import Category

class ExpenseForm(FlaskForm):
    """
    Form for adding an expense
    """
    item = StringField('Item', validators=[DataRequired("Item is required.")])
    cost = DecimalField('Cost', validators=[DataRequired("Cost is required.")])
    category = SelectField('Category', choices=[("1", "one"), ("2", "two")])
    submit = SubmitField('Add')


class BudgetForm(FlaskForm):
    """
    Form for editing budgets
    """
    daily = DecimalField('Daily')
    weekly = DecimalField('Weekly')
    monthly = DecimalField('Monthly')
    # yearly = DecimalField('Yearly')
    submit = SubmitField('Apply')
