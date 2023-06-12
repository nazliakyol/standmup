from flask import make_response, request, render_template, jsonify
from flask_caching import CachedResponse
from sqlalchemy import func
from app.model import videodb, comediandb, tagdb
from app.model.db import pagesSize, db


def handle_tag(tag_id, tag_name):
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

    videos = db.session.query(videodb.Video).filter(videodb.Video.is_active).join(
        videodb.video_tag, videodb.Video.id == videodb.video_tag.c.video_id
    ).join(
        tagdb.Tag, tagdb.Tag.id == videodb.video_tag.c.tag_id
    ).filter(
        tagdb.Tag.id == tag_id,
    ).limit(pagesSize).offset((page - 1) * pagesSize).all()

    tag = db.session.query(tagdb.Tag).filter_by(id= tag_id).first()
    tag_counts = (
        db.session.query(
            tagdb.Tag.name,
            func.count(videodb.Video.id)
        ).join(
            videodb.video_tag,
            tagdb.Tag.id == videodb.video_tag.c.tag_id
        ).join(
            videodb.Video,
            videodb.Video.id == videodb.video_tag.c.video_id
        ).group_by(tagdb.Tag.name).all()
    )
    if tag is None:
        return make_response(jsonify({"error": "Tag not found"}), 404)

    all_tags = db.session.query(tagdb.Tag).order_by(tagdb.Tag.name.asc()).all()

    has_more = True

    if len(videos) < pagesSize:
        has_more = False

    video_count = (db.session.query(func.count(videodb.Video.id)).filter(videodb.Video.is_active).join(videodb.video_tag).filter_by(
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
