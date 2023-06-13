from flask import Blueprint

bp = Blueprint('website', __name__)
pagesSize = 10

from app.route.website import comedian, search, home, tag, video