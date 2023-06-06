from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#import application as app

pagesSize = 10
application = Flask(__name__, template_folder="templates")

application.config["DB_USER"] = "root"
application.config["DB_PASS"] = "zoot"
application.config["DB_HOST"] = "localhost"
# app.config["SQLALCHEMY_ECHO"] = True

application.config.from_prefixed_env()
print(f'env: {application.config["ENV"]}, dbhost: {application.config["DB_HOST"]}')

# connect to db
application.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{application.config['DB_USER']}:{application.config['DB_PASS']}@{application.config['DB_HOST']}/standapi"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)
