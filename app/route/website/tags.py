from flask import make_response,render_template, jsonify
from flask_caching import CachedResponse
from app.model.tag_query import getTags
from app.route.website import bp, cache

# tag page
@bp.route("/tags", methods=["GET"])
@cache.cached(timeout=5000)
def tags():
    all_tags = getTags()
    if all_tags is None:
        return make_response(jsonify({"error": "Tags not found"}), 404)

    for tag in all_tags:
        tag_id = tag.id

    return CachedResponse(
        response=make_response(render_template(
        "tags.html",
        all_tags=all_tags,
        tag_id=tag_id
        )),timeout=5000
    )