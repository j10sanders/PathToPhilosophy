import os
import unittest

import muse

class ResponseTests(unittest.TestCase):
    def test_response(self):
        initial_call = requests.get('https://api-v2.themuse.com/jobs', {'page' : 1})
        self.assertEqual(initial_call, 200)
        self.assertEqual(initial_call, 500)

