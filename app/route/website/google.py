from flask import make_response, jsonify, render_template, request
from flask_caching import CachedResponse
from app.model.comedian_query import getComedianNames, getComedians
from app.route.website import bp, cache
from app.model.tag_query import getTagsWithCounts, getTags

# video page
@bp.route("/google", methods=["GET"])
def google():


    comedians = getComedians()

    all_tags = getTags()

    #for tag in all_tags:
    #    tag_print =
#
    #for comedian in comedians:
    #    comedian_print = print("https://standmup.com/comedians/" + str(comedian.id) + "/" + tag.to_url())


    return render_template(
        "google.html",
        comedians=comedians,
        all_tags=all_tags,
    )

