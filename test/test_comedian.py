import unittest
import sqlite3
from app.model.comedian import Comedian
from app.model.video import Video


class TestComedian(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        self.cursor.execute('CREATE TABLE comedians (name TEXT, description TEXT)')

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_to_dict(self):
        self.cursor.execute("INSERT INTO comedians VALUES ('Tom Papa', 'Test Description')")

        comedian = Comedian("Tom Papa", "Test Description" )

        result = comedian.to_dict()
        self.assertEqual(result['name'], "Tom Papa")
        self.assertEqual(result['description'], "Test Description")

if __name__ == '__main__':
    unittest.main()

