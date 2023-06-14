import unittest
from app.model.tag import Tag

class TestTag(unittest.TestCase):
    def test_to_url(self):
        tag = Tag("326", "amish people", True)

        result = tag.to_url()
        self.assertEqual(result, "amish-people")

if __name__ == '__main__':
    unittest.main()




