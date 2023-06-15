from flask import request, render_template
from app.model.comedian_query import getComedianNames
from app.model.video_query import searchVideos, getSearchVideoCount
from app.route.website import bp, cache, pagesSize
from app.model.tag_query import getTags, getTagsWithCounts


# search page
@bp.route("/search", methods=["GET"])
@cache.cached(timeout=5000)
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
    tag_counts = getTagsWithCounts()

    if search:
        videos = searchVideos(search, page, pagesSize)
        video_count = getSearchVideoCount(search)

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


def search_fail():
    return render_template('search_fail.html')