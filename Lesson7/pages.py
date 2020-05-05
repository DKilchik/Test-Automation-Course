#!/usr/bin/python3
# -*- encoding=utf8 -*-

from page_objects import PageObject
from page_objects import PageElement
from page_objects import MultiPageElement
import time

class GearbestMainPage(PageObject):


    search_text = PageElement(id_='js-iptKeyword')
    search_btn = PageElement(id_='js-btnSubmitSearch')
    banner_close = PageElement(class_name='layui-layer-close')
    region_settings = PageElement(id_='js-labelShipTo')
   

    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)
        self.get('https://www.gearbest.com/')
        self.banner_close.click()
        time.sleep(2)

    def search(self, text):
        self.search_text = text
        self.search_btn.click()
        return GearbestSearchPage(self.w)

    def change_currency(self):

        self.region_settings.click()



class GearbestSearchPage(PageObject):

    results = MultiPageElement(class_name='gbGoodsItem_outBox')

