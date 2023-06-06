import json
from flask import make_response, jsonify, request, render_template, redirect, url_for
from sqlalchemy import func

from app.model import videodb, tagdb, comediandb, youtubeLinkdb
from app.model.db import db


def handle_api():
    return render_template("api.html")

def handle_submit():
    youtube_link = request.form.get('youtube_link')
    message = request.form.get('message')
    video_link = youtubeLinkdb.YoutubeLink(youtube_link=youtube_link, message=message)

    count = db.session.query(func.count(youtubeLinkdb.YoutubeLink.id)).scalar()
    if count > 100:
        print("Server is overload.")
        return redirect(url_for('fail'))

    else:
        if youtube_link is not None:
            if "youtube" in youtube_link:
                db.session.add(video_link)
                db.session.commit()
                return redirect(url_for('success'))
            else:
                print("Invalid YouTube link provided.")
                return redirect(url_for('fail'))
        else:
            print("YouTube link not provided.")
            return redirect(url_for('fail'))


def handle_fail():
    return render_template('fail.html')


def handle_success():
    return render_template('success.html')


def handle_addVideo():
    # if application.config["ENV"] != 'dev':
    #    throw Exception('olala')
    content = request.json

    new_video = videodb.Video(
        comedian_id=content["comedian_id"],
        title=content["title"],
        link=content["link"],
        description=content["description"],
        is_active=content["isActive"],
        is_ready=content["isReady"]
    )

    db.session.add(new_video)
    db.session.commit()

    return json.dumps(new_video.to_dict())


# made some changes here!! how to use video_id and what is the meaning of this error: "
def handle_getVideo(video_id):
    video = videodb.Video.query.get(video_id)
    if video is None:
        return make_response(jsonify({"error": "Video not found"}), 404)
    return json.dumps(video.to_dict())


def handle_getCountByName():
    names = (
        db.session.query(comediandb.Comedian.name, func.count(videodb.Video.id))
            .join(videodb.Video)
            .group_by(comediandb.Comedian.id)
            .all()
    )
    if not names:
        return make_response(jsonify({"error": "No comedians found"}), 404)
    namesToDict = dict((x, y) for x, y in names)
    response = json.dumps(namesToDict)
    return json.dumps(response)



def handle_allComedians():
    comedians = db.session.query(comediandb.Comedian).all()
    if not comedians:
        return make_response(jsonify({"error": "No comedians found"}), 404)
    response = [comedian.to_dict() for comedian in comedians]
    return json.dumps(response)



def handle_getVideoByComedian(id):
    comedians = videodb.Video.query.filter_by(comedian_id=id).all()
    response = [comedian.to_dict() for comedian in comedians]
    return json.dumps(response)


def handle_allVideos():
    args = request.args
    limit = args.get("limit")
    search = args.get("search")

    query = db.session.query(videodb.Video)

    if limit:
        query.limit(limit)
    if search:
        query.filter_by(search)

    videos = query.all()
    response = [video.to_dict() for video in videos]
    return json.dumps(response)



def handle_order_by_random():
    random = videodb.Video.query.order_by(func.random()).first()
    return json.dumps(random.to_dict())


def handle_delete_video(video_id):
    video = videodb.Video.query.get(video_id)
    db.session.delete(video)
    db.session.commit()
    return json.dumps(video.to_dict())



def handle_stat():
    total_video_count = db.session.query(db.func.count(videodb.Video.id)).scalar()
    total_comedian_count = db.session.query(db.func.count(comediandb.Comedian.id)).scalar()
    total_tag_count = db.session.query(db.func.count(tagdb.Tag.id)).scalar()
    names = (
        db.session.query(comediandb.Comedian.id, comediandb.Comedian.name, func.count(videodb.Video.id))
            .join(videodb.Video)
            .group_by(comediandb.Comedian.id)
            .order_by(comediandb.Comedian.name.asc())
            .all()
    )
    result = {
        "total video count": total_video_count,
        "total comedian count": total_comedian_count,
        "total tag count": total_tag_count,
        "video count by comedian": [{"id": id, "name": name, "video count": count} for id, name, count in names]
    }

    return jsonify(result)

