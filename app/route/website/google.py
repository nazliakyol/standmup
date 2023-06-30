from flask import make_response, jsonify, render_template, request
from app.model.comedian_query import  getComedians
from app.route.website import bp
from app.model.tag_query import getTags

@bp.route("/api/google", methods=["GET"])
def google():

    comedians = getComedians()
    for comedian in comedians:
        comedian_link = "https://standmup.com/comedians/" + str(comedian.id)

    all_tags = getTags()
    for tag in all_tags:
        tag_link= "https://standmup.com/comedians/" + str(tag.id) + "/" + tag.to_url()


    result = {
        "tag_link": tag_link,
        "comedian_link": comedian_link,
    }

    return jsonify(result)