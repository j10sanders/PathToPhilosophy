import os
import unittest
import requests
import muse

class ResponseTests(unittest.TestCase):
    def test_response(self):
        initial_call = str(requests.get('https://api-v2.themuse.com/jobs', {'page' : 1}))
        self.assertEqual(initial_call, "<Response [200]>")
        no_page = str(requests.get('https://api-v2.themuse.com/jobs'))
        self.assertEqual(no_page, "<Response [400]>")

if __name__ == "__main__":
    unittest.main()
