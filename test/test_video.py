import unittest
import sqlite3
from flask import Flask

from app.model import db
from app.model.video import Video, video_tag
from app.model.tag import Tag
from app.model.comedian import Comedian


app = Flask(__name__)
db.init_app(app)

class TestVideo(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE comedian (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE tag (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        ''')
        self.cursor.execute('''
                    CREATE TABLE videos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        comedian_id INTEGER,
                        title TEXT,
                        link TEXT,
                        description TEXT,
                        is_active BOOLEAN,
                        is_ready BOOLEAN,
                        FOREIGN KEY (comedian_id) REFERENCES comedian(id)
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE video_tag (
                        video_id INTEGER,
                        tag_id INTEGER,
                        FOREIGN KEY (video_id) REFERENCES videos(id),
                        FOREIGN KEY (tag_id) REFERENCES tag(id)
                    )
                ''')

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_to_dict(self):
        with app.app_context():
            self.cursor.execute("INSERT INTO comedian (name) VALUES ('Tom Papa')")
            self.cursor.execute(
                "INSERT INTO videos (comedian_id, title, link, description, is_active, is_ready) VALUES (1, 'Test Title', 'Test Link', 'Test Description', 0, 0)")

            video = Video("1", "Test Title", "Test Link", "Test Description", False, False)

            result = video.to_dict()
            self.assertEqual(result['comedian_id'], "1")
            self.assertEqual(result['title'], "Test Title")
            self.assertEqual(result['link'], "Test Link")
            self.assertEqual(result['description'], "Test Description")
            self.assertEqual(result['is_active'], False)
            self.assertEqual(result['is_ready'], False)
            self.assertEqual(result['tags'], [])


if __name__ == '__main__':
    unittest.main()
