from flask import make_response, render_template
from flask_caching import CachedResponse

from app.model.comedian_query import  getComedians
from app.route.website import bp
from app.model.tag_query import getTags

@bp.route("/sitemap.txt", methods=["GET"])
def sitemap():
    links = [
        'https://standmup.com'
    ]
    comedians = getComedians()
    for comedian in comedians:
        links.append("https://standmup.com/comedians/" + str(comedian.id))

    all_tags = getTags()
    for tag in all_tags:
        links.append("https://standmup.com/tags/" + str(tag.id) + "/" + tag.to_url())

    resp = make_response(render_template('sitemap.txt', links = links))
    resp.headers['Content-type'] = 'text/plain; charset=utf-8'
    return CachedResponse(
        response=resp,
        timeout=60*60
        )