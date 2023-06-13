import os

from flask import Flask
from app.model import db
from app.service.admin import start_admin
from app.service.auto import start_scheduler

basedir = os.path.abspath(os.path.dirname(__file__))


application = Flask(__name__, template_folder="templates")

application.config["DB_PASS"] = "zoot"
application.config["DB_HOST"] = "localhost"
application.config["DB_USER"] = "root"
# application.config["SQLALCHEMY_ECHO"] = True
application.config.from_prefixed_env()
print(f'env: {application.config["ENV"]}, dbhost: {application.config["DB_HOST"]}')

# connect to db
application.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{application.config['DB_USER']}:{application.config['DB_PASS']}@{application.config['DB_HOST']}/standapi"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(application)

from app.route.api import bp as api_bp
application.register_blueprint(api_bp
                               )
from app.route.website import bp as website_bp
application.register_blueprint(website_bp)

start_scheduler()
if application.config["ENV"] == 'development':
    start_admin()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
