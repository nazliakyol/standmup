from operator import or_

from flask import make_response, jsonify, request, render_template, url_for, redirect
from flask_caching import CachedResponse
from sqlalchemy import func, desc

from app.model import videodb, tagdb, comediandb
from app.model.db import pagesSize, db


def handle_search():
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
    title = search
    all_tags = db.session.query(tagdb.Tag).order_by(tagdb.Tag.name.asc()).all()
    selected_tag = None
    video_count = 0
    videos = []
    if search:
        videos = (
            db.session.query(videodb.Video).filter(videodb.Video.is_active).outerjoin(videodb.video_tag).outerjoin(tagdb.Tag).filter(
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

        video_count = db.session.query(db.func.count(videodb.Video.id)).filter(videodb.Video.is_active).outerjoin(
            videodb.video_tag).outerjoin(tagdb.Tag).filter(
            or_(
                or_(
                    videodb.Video.title.ilike(f"%{search}%"),
                    videodb.Video.description.ilike(f"%{search}%"),
                ),
                tagdb.Tag.name.ilike(f"%{search}%")
            )).scalar()


    if video_count == 0:
        print("Video not found.")
        return render_template('search_fail.html',
                               all_names=names,
                               search=search,
                               all_tags=all_tags,
                               title=title,
                               selected_tag=selected_tag,
                               )

    has_more = True

    if len(videos) < pagesSize:
        has_more = False


    total_pages = int(video_count / pagesSize) + 1

    return render_template('search.html',
        all_videos=videos,
        title = title,
        selected_tag=selected_tag,
        all_names=names,
        page=page,
        search=search,
        has_more=has_more,
        all_tags=all_tags,
        total_pages=total_pages)

def handle_search_fail():
    return render_template('search_fail.html')