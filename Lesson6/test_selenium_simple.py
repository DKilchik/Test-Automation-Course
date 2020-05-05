#!/usr/bin/python3
# -*- encoding=utf8 -*-

# You can find very simple example of the usage Selenium with PyTest in this file.
#
# More info about pytest-selenium:
#    https://pytest-selenium.readthedocs.io/en/latest/user_guide.html
#
# How to run:
#  1) Download geko driver for Chrome here:
#     https://chromedriver.storage.googleapis.com/index.html?path=2.43/
#  2) Install all requirements.txt:
#     pip install -r requirements.txt.txt
#  3) Run tests:
#     python -m pytest -v --driver Chrome --driver-path /tests/chrome test_selenium_simple.py
#

import time


def test_search_example(selenium):
    """ Search some phrase in google and make a screenshot of the page. """

    # Open google search page:
    selenium.get('https://google.com')



    # Find the field for search text input:
    search_input = selenium.find_element_by_name('q')

    # Enter the text for search:
    search_input.clear()
    search_input.send_keys('my first selenium test for Web UI!')



    # Click Search:
    selenium.find_element_by_name('btnK').click()



    # Make the screenshot of browser window:
    selenium.save_screenshot('result.png')
    
