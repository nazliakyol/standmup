from operator import or_

from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func, desc

from app.model import videodb, tagdb, comediandb
from app.model.db import pagesSize, db


def handle_home():
    names = (
        db.session.query(comediandb.Comedian.id, comediandb.Comedian.name, func.count(videodb.Video.id))
            .join(videodb.Video)
            .group_by(comediandb.Comedian.id)
            .order_by(comediandb.Comedian.name.asc())
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
            db.session.query(videodb.Video).filter((videodb.Video.is_active)).outerjoin(videodb.video_tag).outerjoin(tagdb.Tag).filter(
                or_(
                    or_(
                        videodb.Video.title.ilike(f"%{search}%"),
                        videodb.Video.description.ilike(f"%{search}%"),
                    ),
                    tagdb.Tag.name.ilike(f"%{search}%")
                )

            ).order_by(desc(videodb.Video.creation_date))
                .limit(pagesSize)
                .offset((page - 1) * pagesSize)
                .all()
        )
    else:
        videos = (
            db.session.query(videodb.Video).filter((videodb.Video.is_active)).order_by(desc(videodb.Video.creation_date))
                .limit(pagesSize)
                .offset((page - 1) * pagesSize)
                .all()
        )

    has_more = True

    if len(videos) < pagesSize:
        has_more = False

    if videos is None:
        return make_response(jsonify({"error": "Video not found"}), 404)

    all_tags = db.session.query(tagdb.Tag).order_by(tagdb.Tag.name.asc()).all()

    video_count = db.session.query(db.func.count(videodb.Video.id)).scalar()
    total_pages = int(video_count / pagesSize) + 1
    title = 'f*ck other ways to happify'

    return CachedResponse(
        response=make_response(render_template('index.html', all_videos=videos,
        title = title,
        all_names=names,
        page=page,
        search=search,
        has_more=has_more,
        all_tags=all_tags,
        total_pages=total_pages)),
        timeout=5000
    )

