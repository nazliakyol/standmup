import requests
import re
import os
from sqlalchemy.exc import IntegrityError

from app.model import comediandb, video, db
from flask import current_app

basedir = os.path.abspath(os.path.dirname(__file__))

def isMatch(name):
    comedian_names = [comediandb.Comedian.name for comediandb.Comedian in comediandb.Comedian.query.all()]
    for comedian_name in comedian_names:
        if comedian_name == name:
            return True


def getComedianId(name):
    new_comedian = comediandb.Comedian(name=name, description="needed to fill")
    db.session.add(new_comedian)
    db.session.commit()
    id = new_comedian.id
    return id

def runYoutubeAuto():
    with current_app.app_context():
        class YouTube:
            nameRegex = re.compile(".+?(?=--|-|\/|\|)")
            apiKey = current_app.config["YOUTUBE_API_KEY"]
            playlistId = current_app.config["YOUTUBE_PLAYLIST"]
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?key={apiKey}&part=snippet&playlistId={playlistId}"
            response = requests.get(url)
            data = response.json()
            items = data["items"]
            pattern = r"[^a-zA-Z0-9\s]+"


            for item in items:
                itemId = item["id"]
                title = item["snippet"]["title"]
                description = item["snippet"]["description"]
                limited_description = description[:100]
                link = item["snippet"]["resourceId"]["videoId"]
                if title.__contains__("-") or title.__contains__("/") or title.__contains__("|") or title.__contains__("--"):
                    name = re.split(pattern, title)[0]
                else:
                    name = title
                    formatted_name = name.title().rstrip()

                    comedian_id = 0
                    if isMatch(formatted_name):
                        comedian = comediandb.Comedian.query.filter_by(name=formatted_name).first()
                        comedian_id = comedian.id
                    else:
                        comedian_id = getComedianId(formatted_name)

            new_video = video.Video(
                comedian_id=comedian_id,
                title=title,
                link=link,
                description=limited_description,
                is_active=0,
                is_ready=0)
            try:
                db.session.add(new_video)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                error_message = "Duplicate entry error occurred"
                print(error_message + ": " + link)


