from flask import make_response, request, render_template, jsonify
from flask_caching import CachedResponse
from sqlalchemy import func

from app.model.comediandb import Comedian
from app.model import db
from app.model.tagdb import Tag
from app.model.videodb import Video, video_tag
from app.route.website import bp, cache, pagesSize


# tag page
@bp.route("/tags/<tag_id>/<tag_name>", methods=["GET"])
@cache.cached(timeout=5000)
def tag(tag_id, tag_name):
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

    videos = db.session.query(Video).filter(Video.is_active).join(
        video_tag, Video.id == video_tag.c.video_id
    ).join(
        Tag, Tag.id == video_tag.c.tag_id
    ).filter(
        Tag.id == tag_id,
    ).limit(pagesSize).offset((page - 1) * pagesSize).all()

    tag = db.session.query(Tag).filter_by(id= tag_id).first()
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
    if tag is None:
        return make_response(jsonify({"error": "Tag not found"}), 404)

    all_tags = db.session.query(Tag).order_by(Tag.name.asc()).all()

    has_more = True

    if len(videos) < pagesSize:
        has_more = False

    video_count = (db.session.query(func.count(Video.id)).filter(Video.is_active).join(video_tag).filter_by(
        tag_id=tag_id).scalar())

    total_pages = int(video_count / pagesSize) +1
    title = tag.name
    selected_tag = tag
    selected_comedian = None

    return CachedResponse(
        response=make_response(render_template(
        "tag.html",
        title=title,
        selected_tag=selected_tag,
        selected_comedian=selected_comedian,
        all_videos=videos,
        tag=tag,
        tag_counts=tag_counts,
        page=page,
        has_more=has_more,
        all_tags=all_tags,
        all_names=names,
        total_pages=total_pages)),timeout=5000
    )
