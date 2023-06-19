from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from app.model.comedian_query import getComedianNames
from app.model.tag_query import getTags, getTagsWithCounts
from app.model.video_query import getAllVideoCount, searchVideos, getVideos
from app.route.website import bp, cache, pagesSize

# home page
@bp.route("/", methods=["GET"])
@cache.cached(timeout=5000, query_string=True)
def home():
    args = request.args
    page = 1
    if args.get("page") is not None:
        page = int(args.get("page"))

    search = args.get("search")

    videos = []
    if search:
        videos = searchVideos(search, page, pagesSize=10)
    else:
        videos = getVideos(page, pagesSize=10)

    if videos is None:
        return make_response(jsonify({"error": "Video not found"}), 404)

    has_more = True
    if len(videos) < pagesSize:
        has_more = False

    names = getComedianNames()
    all_tags = getTags()
    tag_counts = getTagsWithCounts(0)
    video_count = getAllVideoCount()

    total_pages = int(video_count / pagesSize) + 1
    title = 'light a MUP'
    selected_tag = None
    base_link = "/?"

    return CachedResponse(
        response=make_response(render_template('index.html',
        all_videos=videos,
        title = title,
        selected_tag=selected_tag,
        all_names=names,
        page=page,
        search=search,
        has_more=has_more,
        all_tags=all_tags,
        tag_counts=tag_counts,
        base_link=base_link,
        total_pages=total_pages)),
        timeout=5000
    )

