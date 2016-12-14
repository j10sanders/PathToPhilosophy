import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser


from muse import app


class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        self.process = multiprocessing.Process(target=app.run,
                                               kwargs={"port": 8080})
        self.process.start()
        time.sleep(1)

    def test_no_next(self):
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.fill("location", "New York")
        self.browser.find_option_by_text('Engineering').first.click() 
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
        
    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()