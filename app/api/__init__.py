# app/api/__init__.py

from flask import Blueprint


expenses = Blueprint('api', __name__)

from app.api import expenses
