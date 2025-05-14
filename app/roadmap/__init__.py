from flask import Blueprint

roadmap = Blueprint('roadmap', __name__)

from app.roadmap import routes
from app.roadmap import ai_routes
from app.roadmap import custom_routes
