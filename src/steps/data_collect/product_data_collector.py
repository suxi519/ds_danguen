import time
import selenium

from selenium import webdriver
from utils.util_path import PathUtils


class ProductDataCollector:
    def __init__(self):
        print(PathUtils.driver_path())
        self.driver = webdriver.Chrome(executable_path=PathUtils.driver_path())

    def enter(self):
        self.driver.get('https://www.daangn.com/')

    def search_village(self, village_name):
        time.sleep(1)
        id_search_bar = 'header-search-input'
        id_search_btn = 'header-search-button'
        search_bar = self.driver.find_element_by_id(id_search_bar)
        search_btn = self.driver.find_element_by_id(id_search_btn)
        search_bar.send_keys(village_name)
        search_btn.click()

    def get_product_link(self):
        class_product_link = 'flea-market-article-link'
        elements = self.driver.find_elements_by_class_name(class_product_link)
        return [element.get_attribute('href') for element in elements]

    def enter_product_link(self, link, sleep=2):
        time.sleep(sleep)
        self.driver.get(link)


c = ProductDataCollector()
c.enter()
c.search_village('상현동')
for idx, link in enumerate(c.get_product_link()):
    c.enter_product_link(link)
    if idx == 5:
        break

c.search_village('정자동')
for idx, link in enumerate(c.get_product_link()):
    c.enter_product_link(link)
    if idx == 5:
        break
