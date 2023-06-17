from flask import make_response,render_template, jsonify
from flask_caching import CachedResponse
from app.model.comedian_query import getComedians
from app.route.website import bp, cache

# tag page
@bp.route("/comedians", methods=["GET"])
@cache.cached(timeout=5000)
def comedians():
    all_comedians = getComedians()
    if all_comedians is None:
        return make_response(jsonify({"error": "Comedians not found"}), 404)

    for comedian in all_comedians:
        comedian_id = comedian.id

    return CachedResponse(
        response=make_response(render_template(
        "comedians.html",
        all_comedians=all_comedians,
        comedian_id=comedian_id
        )),timeout=5000
    )
