import unittest
from app.model.comedian import Comedian
from app.model.video import Video


class TestComedian(unittest.TestCase):
    def test_to_dict(self):
        comedian = Comedian("Tom Papa", "Test Description" )

        result = comedian.to_dict()
        self.assertEqual(result['name'], "Tom Papa")
        self.assertEqual(result['description'], "Test Description")

if __name__ == '__main__':
    unittest.main()

