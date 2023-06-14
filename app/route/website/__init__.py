from flask import Blueprint
from flask_caching import Cache

bp = Blueprint('website', __name__, template_folder='templates')
cache = Cache()
pagesSize = 10

from app.route.website import comedian, search, home, tag, video