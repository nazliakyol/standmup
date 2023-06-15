from operator import not_

from flask import make_response, jsonify, request, render_template
from flask_caching import CachedResponse
from sqlalchemy import func
from app.model.comedian import Comedian
from app.model import db
from app.model.comedian_query import getComedianNames
from app.model.tag import Tag
from app.model.video import Video, video_tag
from app.model.video_query import getVideos, getVideoById, getOtherVideos, getVideosByComedianId
from app.route.website import bp, cache, pagesSize
from app.model.tag_query import getTagsWithCounts, getTags

# video page
@bp.route("/videos/<video_id>", methods=["GET"])
@cache.cached(timeout=5000)
def video(video_id):

    names = getComedianNames()

    video = getVideoById(video_id)
    if video is None:
        return make_response(jsonify({"error": "Video not found"}), 404)

    other_videos = getOtherVideos(video.id, 30)

    video_tags = video.getTags()

    comedian_videos = getVideosByComedianId(Video.comedian_id, page=1, pagesSize=10)

    all_tags = getTags()
    tag_counts = getTagsWithCounts(0)

    title = video.title + " by " + video.comedian.name

    selected_name = None
    selected_tag = None


    return CachedResponse(
        response=make_response(render_template(
        "video.html",
        title=title,
        selected_tag=selected_tag,
        tag_counts=tag_counts,
        selected_name=selected_name,
        all_videos=[video],
        other_videos=other_videos,
        all_names=names,
        video=video,
        comedian_videos=comedian_videos,
        video_tags=video_tags,
        all_tags=all_tags)), timeout=5000
    )

