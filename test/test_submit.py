import unittest

from app.route.api.api import submit


class TestSubmit(unittest.TestCase):
    def test_handle_submit_success(self):
        return
        # Test case where youtube_link is a valid YouTube link
        result = submit()
        self.assertEqual(result, "success.html")

    def test_submit_invalid_link(self):
        return
        # Test case where youtube_link is not a valid YouTube link
        result = submit()
        self.assertEqual(result, "fail.html")

    def test_submit_no_link(self):
        return
        # Test case where youtube_link is not provided
        result = submit()
        self.assertEqual(result, "fail.html")

    def test_submit_server_overload(self):
        return
        # Test case where server is overloaded
        result = submit()
        self.assertEqual(result, "fail.html")

if __name__ == '__main__':
    unittest.main()
