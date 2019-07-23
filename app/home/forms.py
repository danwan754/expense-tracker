# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired

# from ..models import Category

class ExpenseForm(FlaskForm):
    """
    Form for adding an expense
    """
    item = StringField('Item', validators=[DataRequired("Item is required.")])
    cost = DecimalField('Cost', validators=[DataRequired("Cost is required.")])
    category = SelectField('Category', choices=[("Food", "Food"), ("Entertainment", "Entertainment"), ("Health", "Health"), ("Debt", "Debt"), ("Gift", "Gift"), ("Education", "Education"), ("Travel", "Travel"), ("Other", "Other")])
    date = DateField('Date', validators=[DataRequired("Date is required.")])
    submit = SubmitField('Add')


class BudgetForm(FlaskForm):
    """
    Form for editing budgets
    """
    dailyBudgetField = DecimalField('Daily')
    weeklyBudgetField = DecimalField('Weekly')
    monthlyBudgetField = DecimalField('Monthly')
    yearlyBudgetField = DecimalField('Yearly')
    submitBudgetField = SubmitField('Apply')
