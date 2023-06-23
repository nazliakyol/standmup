from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse

from app.model.comedian import Comedian
from app.model.comedian_query import getComedianNames, getComedianById
from app.model.product_query import getProductsByComedianId, getProducts
from app.model.video_query import getVideosByComedianId, getVideoCountByComedianId
from app.model.tag_query import getTags, getTagsWithCounts
from app.route.website import bp, cache, pagesSize


@bp.route("/comedians/<comedian_id>", methods=["GET"])
@cache.cached(timeout=5000, query_string=True)
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
    tag_counts = getTagsWithCounts(5)

    has_more = True
    if len(videos) < pagesSize:
        has_more = False
    total_pages = int(video_count / pagesSize) + 1
    title = comedian.name
    selected_name = None
    selected_tag = None
    selected_comedian = comedian.name

    all_products = getProducts()
    if all_products is None:
        return make_response(jsonify({"error": "No product found"}), 404)

    comedian_products = getProductsByComedianId(comedian_id)

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
        comedian_products=comedian_products,
        all_tags=all_tags)), timeout=5000
    )

