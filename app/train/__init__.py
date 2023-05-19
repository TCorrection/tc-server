from flask import Blueprint

bp = Blueprint('train', __name__)

from app.train import routes
