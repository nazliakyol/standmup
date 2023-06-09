from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func
from app.model import videodb, tagdb, comediandb
from app.model.db import pagesSize, db


def handle_comedian(comedian_id):
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
            .filter_by(comedian_id=comedian_id)
            .limit(pagesSize)
            .offset((page - 1) * pagesSize)
            .all()
    )

    comedian = db.session.query(comediandb.Comedian).filter_by(id= comedian_id).first()
    if comedian is None:
        return make_response(jsonify({"error": "Comedian not found"}), 404)

    all_tags = db.session.query(tagdb.Tag).order_by(tagdb.Tag.name.asc()).all()


    has_more = True

    if len(videos) < pagesSize:
        has_more = False

    video_count = (db.session.query(func.count(videodb.Video.id))
            .filter(videodb.Video.is_active)
            .filter_by(comedian_id=comedian_id)
            .scalar()
    )
    total_pages = int(video_count / pagesSize) + 1
    title = comedian.name
    selected_name = None
    selected_tag = None

    selected_comedian = comedian.name
    return CachedResponse(
        response=make_response(render_template(
        "comedian.html",
        title=title,
        selected_name=selected_name,
        selected_tag=selected_tag,
        selected_comedian=selected_comedian,
        all_videos=videos,
        all_names=names,
        page=page,
        has_more=has_more,
        comedian=comedian,
        comedian_name=comedian.name,
        total_pages=total_pages,
        comedian_description=comedian.description,
        all_tags=all_tags)), timeout=5000
    )

