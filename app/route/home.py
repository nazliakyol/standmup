from operator import or_

from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func, desc

from app.model.comediandb import Comedian
from app.model.db import db
from app.model.tagdb import Tag
from app.model.videodb import Video, video_tag
from application import pagesSize


def handle_home():
    names = (
        db.session.query(Comedian.id, Comedian.name, func.count(Video.id))
            .join(Video)
            .group_by(Comedian.id)
            .order_by(Comedian.name.asc())
            .all()
    )

    if not names:
        return make_response(jsonify({"error": "No comedians found"}), 404)

    args = request.args

    page = 1
    if args.get("page") is not None:
        page = int(args.get("page"))

    search = args.get("search")

    videos = []
    if search:
        videos = (
            db.session.query(Video).filter((Video.is_active)).outerjoin(video_tag).outerjoin(Tag).filter(
                or_(
                    or_(
                        Video.title.ilike(f"%{search}%"),
                        Video.description.ilike(f"%{search}%"),
                    ),
                    Tag.name.ilike(f"%{search}%")
                )

            ).order_by(desc(Video.creation_date))
                .limit(pagesSize)
                .offset((page - 1) * pagesSize)
                .all()
        )
    else:
        videos = (
            db.session.query(Video).filter((Video.is_active)).order_by(desc(Video.creation_date))
                .limit(pagesSize)
                .offset((page - 1) * pagesSize)
                .all()
        )

    has_more = True

    if len(videos) < pagesSize:
        has_more = False

    if videos is None:
        return make_response(jsonify({"error": "Video not found"}), 404)

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
    video_count = db.session.query(db.func.count(Video.id)).scalar()
    total_pages = int(video_count / pagesSize) + 1
    title = 'f*ck other ways to happy'
    selected_tag = None


    return CachedResponse(
        response=make_response(render_template('./templates/index.html', all_videos=videos,
        title = title,
        selected_tag=selected_tag,
        all_names=names,
        page=page,
        search=search,
        has_more=has_more,
        all_tags=all_tags,
        tag_counts=tag_counts,
        total_pages=total_pages)),
        timeout=5000
    )

