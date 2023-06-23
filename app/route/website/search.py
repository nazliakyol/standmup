from flask import request, render_template, make_response
from flask_caching import CachedResponse
from app.model.comedian_query import getComedianNames
from app.model.video_query import searchVideos, getSearchVideoCount
from app.route.website import bp, pagesSize, cache
from app.model.tag_query import getTags, getTagsWithCounts


# search page
@bp.route("/search", methods=["GET"])
@cache.cached(timeout=5000, query_string=True)
def search():
    args = request.args

    page = 1
    if args.get("page") is not None:
        page = int(args.get("page"))

    search = args.get("search")

    video_count = 0
    videos = []

    names = getComedianNames()

    title = search
    all_tags = getTags()
    selected_tag = None
    tag_counts = getTagsWithCounts(5)

    if search:
        videos = searchVideos(search, page, pagesSize =10)
        video_count = getSearchVideoCount(search)
        total_pages = int(video_count / pagesSize) + 1

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

    base_link = "/search?search=" + search

    return CachedResponse(
        response=make_response(render_template('search.html',
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
        timeout=5000)


# search fail page
@bp.route("/search", methods=["GET"])
@cache.cached(timeout=5000, query_string=True)
def search_fail():
    return CachedResponse(
        response=make_response(render_template('search_fail.html')),
        timeout=5000)