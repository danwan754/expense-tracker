# app/api/__init__.py

from flask import Blueprint


bp = Blueprint('api', __name__)

from app.api import users