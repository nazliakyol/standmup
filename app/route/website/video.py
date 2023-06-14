from operator import not_

from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func
from app.model.comedian import Comedian
from app.model import db
from app.model.tag import Tag
from app.model.video import Video, video_tag
from app.route.website import bp, cache, pagesSize


# video page
@bp.route("/videos/<video_id>", methods=["GET"])
@cache.cached(timeout=5000)
def video(video_id):
    names = (
        db.session.query(Comedian.id, Comedian.name, func.count(Video.id))
            .join(Video)
            .group_by(Comedian.id)
            .order_by(Comedian.name.asc())
            .all()
    )

    args = request.args
    page = 1
    if args.get("page") is not None:
        page = int(args.get("page"))

    videos = (
        db.session.query(Video).filter((Video.is_active))
            .filter_by(id=video_id)
            .limit(pagesSize)
            .offset((page - 1) * pagesSize)
            .all()
    )

    has_more = True

    if len(videos) < pagesSize:
        has_more = False
    video = db.session.query(Video).filter_by(id=video_id).first()
    other_videos = (
        db.session.query(Video)
            .filter(Video.is_active)
            .filter(not_(Video.id == videos[videos.index(video)].id))
            .limit(30)
            .all()
    )

    video_tags = video.getTags()
    if video is None:
        return make_response(jsonify({"error": "Video not found"}), 404)

    comedian_videos = db.session.query(Video).join(Comedian).filter(
        Video.comedian_id == Comedian.id
    ).all()

    all_tags = db.session.query(Tag).order_by(Tag.name.asc()).all()
    tag_counts = (
        db.session.query(
            Tag.name,
            func.count(Video.id)
        ).join(
            video_tag,
            Tag.id == video_tag.c.tag_id
        ).join(
            Video,
            Video.id == video_tag.c.video_id
        ).group_by(Tag.name).all()
    )
    title = video.title + " by " + video.comedian.name

    selected_name = None
    selected_tag = None


    return CachedResponse(
        response=make_response(render_template(
        "video.html",
        title=title,
        selected_tag=selected_tag,
        tag_counts=tag_counts,
        selected_name=selected_name,
        all_videos=videos,
        other_videos=other_videos,
        all_names=names,
        page=page,
        has_more=has_more,
        video=video,
        comedian_videos=comedian_videos,
        video_tags=video_tags,
        all_tags=all_tags)), timeout=5000
    )

