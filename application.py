import os

from flask import Flask
from app.model import db
from app.service.admin import start_admin
#from app.service.scheduler import start_scheduler
from app.route.api import bp as api_bp
from app.route.website import bp as website_bp, cache


basedir = os.path.abspath(os.path.dirname(__file__))

application = Flask(__name__, template_folder="templates")

# config

application.config.from_prefixed_env()
debug = application.config["ENV"] == 'development'

# connect to db
application.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{application.config['DB_USER']}:{application.config['DB_PASS']}@{application.config['DB_HOST']}/standapi"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
if debug:
    application.config["SQLALCHEMY_ECHO"] = True

cacheType = "SimpleCache"
if debug:
    cacheType = "NullCache"
config = {
    "DEBUG": debug,          # some Flask specific configs
    "CACHE_TYPE": cacheType,
    "CACHE_DEFAULT_TIMEOUT": 300
}
application.config.from_mapping(config)
print(f'env: {application.config["ENV"]}, dbhost: {application.config["DB_HOST"]}')

# db
db.init_app(application)

# routes
application.register_blueprint(api_bp)
application.register_blueprint(website_bp)

# cache
cache.init_app(application)

# start_scheduler()
if application.config["ENV"] == 'development':
    start_admin(application)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
