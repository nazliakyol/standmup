from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func
from app.model.comedian import Comedian, getComedianNames, getComedianById
from app.model.tag import Tag, getTags, getTagsWithCounts
from app.model.video import Video, video_tag, getVideosByComedianId, getVideoCountByComedianId
from app.route.website import bp, cache, pagesSize
from app.model import db

# comedian page
@bp.route("/comedians/<comedian_id>", methods=["GET"])
@cache.cached(timeout=5000)
def comedian(comedian_id):
    args = request.args
    page = 1
    if args.get("page") is not None:
        page = int(args.get("page"))

    videos = getVideosByComedianId(comedian_id, page, pagesSize)
    comedian = getComedianById(comedian_id)
    if comedian is None:
        return make_response(jsonify({"error": "Comedian not found"}), 404)
    video_count = getVideoCountByComedianId(comedian_id)

    names = getComedianNames()
    all_tags = getTags()
    tag_counts = getTagsWithCounts()

    has_more = True
    if len(videos) < pagesSize:
        has_more = False
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

