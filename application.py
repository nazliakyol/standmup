from flask import Flask
from app.model import db
from app.route.api import bp as api_bp
from app.route.website import bp as website_bp, cache

# from app.service.admin import start_admin

app = Flask(__name__, template_folder="templates")

# config
app.config.from_prefixed_env()
debug = "ENV" in app.config and app.config["ENV"] == "development"

# connect to db
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{app.config['DB_USER']}:{app.config['DB_PASS']}@{app.config['DB_HOST']}/standapi"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
if debug:
    app.config["SQLALCHEMY_ECHO"] = True

cacheType = "SimpleCache"
if debug:
    cacheType = "NullCache"
config = {
    "DEBUG": debug,  # some Flask specific configs
    "CACHE_TYPE": cacheType,
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app.config.from_mapping(config)
print(f'env: {app.config["ENV"]}, dbhost: {app.config["DB_HOST"]}')

# db
db.init_app(app)

# routes
app.register_blueprint(api_bp)
app.register_blueprint(website_bp)

# cache
cache.init_app(app)

# if app.config["ENV"] == "development":
#     start_admin(app)
# else:
#    start_scheduler()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
