import os

from flask import make_response, jsonify, Flask

from app.route.api import handle_api, handle_submit, handle_fail, handle_success, handle_addVideo, handle_getVideo, \
    handle_getCountByName, handle_allComedians, handle_getVideoByComedian, handle_allVideos, handle_order_by_random, \
    handle_delete_video, handle_stat
from app.route.comedian import handle_comedian
from app.route.home import handle_home
from app.route.search import handle_search
from app.route.tag import handle_tag
from app.route.video import handle_video
from app.service.admin import start_admin
from app.service.auto import start_scheduler
from app.service.cache import cache

basedir = os.path.abspath(os.path.dirname(__file__))
pagesSize = 10

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

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(application)

# home page
@application.route("/", methods=["GET"])
@cache.cached(timeout=5000)
def home():
    return handle_home()


# search page
@application.route("/search", methods=["GET"])
@cache.cached(timeout=5000)
def search():
    return handle_search()


# tag page
@application.route("/tags/<tag_id>/<tag_name>", methods=["GET"])
@cache.cached(timeout=5000)
def tag(tag_id, tag_name):
    return handle_tag(tag_id, tag_name)


# comedian page
@application.route("/comedians/<comedian_id>", methods=["GET"])
@cache.cached(timeout=5000)
def comedian(comedian_id):
    return handle_comedian(comedian_id)


# video page
@application.route("/videos/<video_id>", methods=["GET"])
@cache.cached(timeout=5000)
def video(video_id):
    return handle_video(video_id)


# api page
@application.route("/api")
def api():
    return handle_api()


# submit form page
@application.route('/api/submit', methods=['POST'])
def submit():
    return handle_submit()


# submit fail page
@application.route('/api/fail')
def fail():
    return handle_fail()


# submit success page
@application.route('/api/success')
def success():
    return handle_success()


# add video
@application.route("/api/videos", methods=["POST"])
def addVideo():
    if application.config["ENV"] == 'development':
        return handle_addVideo()
    else:
        return make_response(jsonify({"error": "Not authorized."}), 401)


# get video by id
@application.route("/api/videos/<video_id>", methods=["GET"])
def getVideo(video_id):
    return handle_getVideo(video_id)


# get all comedian names with count
@application.route("/api/comedians", methods=["GET"])
def getCountByName():
    return handle_getCountByName()


# get all comedians
@application.route("/api/comedians/all", methods=["GET"])
def allComedians():
    return handle_allComedians()


# get videos by comedian
@application.route("/api/comedians/<id>/videos", methods=["GET"])
def getVideoByComedian():
    return handle_getVideoByComedian()


# get all videos
@application.route("/api/videos/all", methods=["GET"])
def allVideos():
    return handle_allVideos()


# get random video
@application.route("/api/random", methods=["GET"])
def orderByRandom():
    return handle_order_by_random()


# delete video by id
@application.route("/api/videos/<video_id>", methods=["DELETE"])
def delete():
    if application.config["ENV"] == 'development':
        return handle_delete_video()
    else:
        return make_response(jsonify({"error": "Not authorized."}), 401)


# show stat
@application.route("/api/stat", methods=["GET"])
def stat():
    return handle_stat()


start_scheduler()
if application.config["ENV"] == 'development':
    start_admin()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
