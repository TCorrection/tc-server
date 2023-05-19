from flask import Blueprint

bp = Blueprint('correction', __name__)

from app.correction import routes
