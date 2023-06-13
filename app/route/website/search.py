from operator import or_

from flask import make_response, jsonify, request, render_template
from sqlalchemy import func, desc

from app.model.comediandb import Comedian
from app.model import db
from app.model.tagdb import Tag
from app.model.videodb import Video, video_tag
from app.service.cache import cache
from app.route.website import bp, pagesSize

# search page
@bp.route("/search", methods=["GET"])
@cache.cached(timeout=5000)
def handle_search():
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
    title = search
    all_tags = db.session.query(Tag).order_by(Tag.name.asc()).all()
    selected_tag = None
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
    video_count = 0
    videos = []
    if search:
        videos = (
            db.session.query(Video).filter(Video.is_active).outerjoin(video_tag).outerjoin(Tag).filter(
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

        video_count = db.session.query(db.func.count(Video.id)).filter(Video.is_active).outerjoin(
            video_tag).outerjoin(Tag).filter(
            or_(
                or_(
                    Video.title.ilike(f"%{search}%"),
                    Video.description.ilike(f"%{search}%"),
                ),
                Tag.name.ilike(f"%{search}%")
            )).scalar()


    if video_count == 0:
        print("Video not found.")
        return render_template('search_fail.html',
                               all_names=names,
                               search=search,
                               all_tags=all_tags,
                               title=title,
                               selected_tag=selected_tag,
                               tag_counts=tag_counts
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
        tag_counts=tag_counts,
        total_pages=total_pages)

def handle_search_fail():
    return render_template('search_fail.html')