from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func
from app.model.comediandb import Comedian
from app.model.tagdb import Tag
from app.model.videodb import Video, video_tag
from app.route.website import bp, cache, pagesSize
from app.model import db

# comedian page
@bp.route("/comedians/<comedian_id>", methods=["GET"])
@cache.cached(timeout=5000)
def comedian(comedian_id):
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
            .filter_by(comedian_id=comedian_id)
            .limit(pagesSize)
            .offset((page - 1) * pagesSize)
            .all()
    )

    comedian = db.session.query(Comedian).filter_by(id= comedian_id).first()
    if comedian is None:
        return make_response(jsonify({"error": "Comedian not found"}), 404)

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

    has_more = True

    if len(videos) < pagesSize:
        has_more = False

    video_count = (db.session.query(func.count(Video.id))
            .filter(Video.is_active)
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
        tag_counts=tag_counts,
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

