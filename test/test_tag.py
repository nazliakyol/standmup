import unittest
import sqlite3
from app.model.tag import Tag

class TestTag(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        self.cursor.execute('CREATE TABLE tags (id TEXT, name TEXT, is_visible BOOLEAN)')

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_to_dict(self):
        self.cursor.execute("INSERT INTO tags VALUES ('1', 'Test Tag', 'False')")

        tag = Tag("1", "Test Tag", "False" )

        result = tag.to_dict()
        self.assertEqual(result['id'], '1')
        self.assertEqual(result['name'], "Test Tag")
        self.assertEqual(result['is_visible'], "False")

    def test_to_url(self):
        tag = Tag( "1", "Test Tag", False)

        result = tag.to_url()
        self.assertEqual(result, "Test-Tag")

if __name__ == '__main__':
    unittest.main()




