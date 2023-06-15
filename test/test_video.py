import os

from flask import Flask

from app.model import db
from app.model.video import Video, video_tag
from app.model.tag import Tag
from app.model.comedian import Comedian


import unittest
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

class TestVideo(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def test_to_dict(self):
        comedian = Comedian('Test Comedian', 'Test Description')
        comedian.id = 1
        video = Video(1, "Test Title", "Test Link", "Test Description", False, False)
        video.comedian = comedian

        result = video.to_dict()
        self.assertEqual(result['comedian_id'], 1)
        self.assertEqual(result['title'], "Test Title")
        self.assertEqual(result['link'], "Test Link")
        self.assertEqual(result['description'], "Test Description")
        self.assertEqual(result['is_active'], False)
        self.assertEqual(result['is_ready'], False)
        self.assertEqual(result['tags'], [])
