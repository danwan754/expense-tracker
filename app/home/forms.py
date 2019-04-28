# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired

# from ..models import Category

class ExpenseForm(FlaskForm):
    """
    Form for adding an expense
    """
    item = StringField('Item', validators=[DataRequired()])
    cost = DecimalField('Cost', validators=[DataRequired()])
    category = SelectField('Category', choices=[("1", "one"), ("2", "two")])
    submit = SubmitField('Add')
