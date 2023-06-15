import unittest

from flask import json, Flask

from app.model import video, db
from app.route.api.api import addVideo

class TestAddVideo(unittest.TestCase):
    def test_addVideo(self):
        return

        content = {
            "comedian_id": 1,
            "title": "Test Video",
            "link": "https://www.youtube.com/watch?v=DJiO2A4NNnM",
            "description": "Test description",
            "isActive": False,
            "isReady": False
        }

        new_video = video.Video(
            comedian_id=content["comedian_id"],
            title=content["title"],
            link=content["link"],
            description=content["description"],
            is_active=content["isActive"],
            is_ready=content["isReady"]
        )

        db.session.add(new_video)
        db.session.commit()

        result = addVideo()

        result_dict = json.loads(result)

        # Assert the expected values
        self.assertEqual(result_dict["comedian_id"], 1)
        self.assertEqual(result_dict["title"], "Test Video")
        self.assertEqual(result_dict["link"], "https://www.youtube.com/watch?v=DJiO2A4NNnM")
        self.assertEqual(result_dict["description"], "Test description")
        self.assertEqual(result_dict["is_active"], False)
        self.assertEqual(result_dict["is_ready"], False)

if __name__ == '__main__':
    unittest.main()
