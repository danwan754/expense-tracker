# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'))
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'))


    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Budget(db.Model):
    """
    Create a Budget table
    """

    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    daily = db.Column(db.Float)
    monthly = db.Column(db.Float)
    yearly = db.Column(db.Float)
    january = db.Column(db.Float)
    february = db.Column(db.Float)
    march = db.Column(db.Float)
    april = db.Column(db.Float)
    may = db.Column(db.Float)
    june = db.Column(db.Float)
    july = db.Column(db.Float)
    august = db.Column(db.Float)
    september = db.Column(db.Float)
    october = db.Column(db.Float)
    november = db.Column(db.Float)
    december = db.Column(db.Float)


    def __repr__(self):
        return '<Budget: {}>'.format(self.name)


class Expense(db.Model):
    """
    Create a Expense table
    """

    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(60))
    cost = db.Column(db.Float)
    category = db.Column(db.String(60))
    date = db.Column(db.Date)

    def __repr__(self):
        return '<Expense: {}>'.format(self.name)
