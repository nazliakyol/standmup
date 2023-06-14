import unittest
from app.model.video import Video


class TestVideo(unittest.TestCase):

    def test_to_dict(self):
        return

        video = Video("1", "Test title", "DJiO2A4NNnM", "Test Description", False, False)

        result = video.to_dict()
        self.assertEqual(result['comedian_id'], "1")
        self.assertEqual(result['title'], "Test title")
        self.assertEqual(result['link'], "DJiO2A4NNnM")
        self.assertEqual(result['description'], "Test Description")
        self.assertEqual(result['is_active'], False)
        self.assertEqual(result['is_ready'], False)

if __name__ == '__main__':
    unittest.main()
