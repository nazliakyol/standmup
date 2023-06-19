from flask import make_response, request, render_template, jsonify
from flask_caching import CachedResponse
from app.model.comedian_query import getComedianNames
from app.model.tag_query import getTagVideos, getTagById, getTagsWithCounts, getTags
from app.route.website import bp, cache, pagesSize
from app.model.video_query import getVideoCountByTagId

# tag page
@bp.route("/tags/<tag_id>/<tag_name>", methods=["GET"])
@cache.cached(timeout=5000, query_string=True)
def tag(tag_id, tag_name):
    args = request.args

    page = 1
    if args.get("page") is not None:
        page = int(args.get("page"))

    names = getComedianNames()
    videos = getTagVideos(tag_id, page, pagesSize)

    tag = getTagById(tag_id)
    if tag is None:
        return make_response(jsonify({"error": "Tag not found"}), 404)

    tag_counts = getTagsWithCounts(5)

    all_tags = getTags()

    has_more = True
    if len(videos) < pagesSize:
        has_more = False

    video_count = getVideoCountByTagId(tag_id)

    total_pages = int(video_count / pagesSize) +1
    title = tag.name
    selected_tag = tag
    selected_comedian = None
    base_link = "/tags/" + str(tag.id) + "/" + tag.to_url() + "?"

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
        base_link=base_link,
        total_pages=total_pages)),timeout=5000
    )
