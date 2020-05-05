#!/usr/bin/python3
# -*- encoding=utf8 -*-

#     Run tests:
#     python -m pytest -v --driver Chrome --driver-path /tests/chrome test_selenium_simple.py
import time

def test_hello_selenium(selenium):
    """  Hello,Selenium!!! """

    #Open InStat main page
    selenium.get('https://instatsport.com/')

    time.sleep(3)

    #Find input field for email
    mail_input = selenium.find_element_by_class_name('')

    #Enter invalid text into inout field
    mail_input.clear()
    mail_input.send_keys('Invalid email')

    # Make the screenshot of browser window:
    selenium.save_screenshot('result.png')




