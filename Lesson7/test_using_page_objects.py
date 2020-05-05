#!/usr/bin/python3
# -*- encoding=utf8 -*-

from .pages import GearbestMainPage


def test_check_number_of_results(web_browser):

    page = GearbestMainPage(web_browser)
    search_page = page.search('laptop')

    assert len(search_page.results) == 36, 'Not enough results found!'

