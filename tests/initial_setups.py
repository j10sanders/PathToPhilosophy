import os
import unittest
import requests
from flask import url_for
import muse
from muse.views import *

class ResponseTests(unittest.TestCase):
    def test_response(self):
        initial_call = str(requests.get('https://api-v2.themuse.com/jobs', {'page' : 1}))
        self.assertEqual(initial_call, "<Response [200]>")
        no_page = str(requests.get('https://api-v2.themuse.com/jobs'))
        self.assertEqual(no_page, "<Response [400]>")
    
    def test_views(self):
        id = "49571"
        rv = muse.views.listing_get(id)
        self.assertEqual(rv.status, '302 FOUND')

        
if __name__ == "__main__":
    unittest.main()
