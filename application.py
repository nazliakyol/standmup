import os

from flask import Flask
from app.model import db

basedir = os.path.abspath(os.path.dirname(__file__))

application = Flask(__name__, template_folder="templates")

# config
application.config["DB_PASS"] = "zoot"
application.config["DB_HOST"] = "localhost"
application.config["DB_USER"] = "root"
# application.config["SQLALCHEMY_ECHO"] = True
application.config.from_prefixed_env()
debug = application.config["ENV"] == 'development'

# connect to db
application.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{application.config['DB_USER']}:{application.config['DB_PASS']}@{application.config['DB_HOST']}/standapi"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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


db.init_app(application)

from app.route.api import bp as api_bp
from app.route.website import bp as website_bp, cache

application.register_blueprint(api_bp)
application.register_blueprint(website_bp)
cache.init_app(application)

# from app.service.admin import start_admin
# from app.service.auto import start_scheduler
# start_scheduler()
# if application.config["ENV"] == 'development':
#     start_admin()
#
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
