from operator import not_

from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func
from app.model import videodb, tagdb, comediandb
from app.model.db import pagesSize, db


def handle_video(video_id):
    names = (
        db.session.query(comediandb.Comedian.id, comediandb.Comedian.name, func.count(videodb.Video.id))
            .join(videodb.Video)
            .group_by(comediandb.Comedian.id)
            .order_by(comediandb.Comedian.name.asc())
            .all()
    )

    args = request.args
    page = 1
    if args.get("page") is not None:
        page = int(args.get("page"))

    videos = (
        db.session.query(videodb.Video).filter((videodb.Video.is_active))
            .filter_by(id=video_id)
            .limit(pagesSize)
            .offset((page - 1) * pagesSize)
            .all()
    )

    has_more = True

    if len(videos) < pagesSize:
        has_more = False
    video = db.session.query(videodb.Video).filter_by(id=video_id).first()
    other_videos = (
        db.session.query(videodb.Video)
            .filter(videodb.Video.is_active)
            .filter(not_(videodb.Video.id == videos[videos.index(video)].id))
            .limit(30)
            .all()
    )

    video_tags = video.getTags()
    video_title = db.session.query(videodb.Video.title).filter_by(id= video_id).first()
    if video is None:
        return make_response(jsonify({"error": "Video not found"}), 404)

    comedian_videos = db.session.query(videodb.Video).join(comediandb.Comedian).filter(
        videodb.Video.comedian_id == comediandb.Comedian.id
    ).all()

    all_tags = db.session.query(tagdb.Tag).order_by(tagdb.Tag.name.asc()).all()

    video_count = (db.session.query(func.count(videodb.Video.id))
            .filter(videodb.Video.is_active)
            .filter_by(id=video_id)
            .scalar()
    )
    total_pages = int(video_count / pagesSize) + 1

    title = video.title + " by " + video.comedian.name


    return CachedResponse(
        response=make_response(render_template(
        "video.html",
        title=title,
        all_videos=videos,
        other_videos=other_videos,
        all_names=names,
        page=page,
        video_count=video_count,
        has_more=has_more,
        video=video,
        comedian_videos=comedian_videos,
        video_title=video_title,
        total_pages=total_pages,
        video_tags=video_tags,
        all_tags=all_tags)), timeout=5000
    )

