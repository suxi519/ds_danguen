import time
import selenium

from selenium import webdriver

from src.steps.data_collect.location_notifier import LocationNotifier
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
        try:
            elements = self.driver.find_elements_by_class_name(class_product_link)
        except:
            return []
        return [element.get_attribute('href') for element in elements]

    def enter_product_link(self, link, sleep=2):
        time.sleep(sleep)
        self.driver.get(link)

    def get_product_information(self):

        def parse_temperature(temperature):
            return float(temperature[5:-3])

        def parse_category(category: str):
            return category.split(' ∙ ')[0]

        def parse_price(price: str):
            return 0 if price=='가격없음' else int(price.replace(',', '')[:-1])

        def parse_counts(counts: str):
            def join_char(s: str):
                return int(''.join([c for c in s if c.isnumeric()]))
            return list(map(join_char, counts.split(' ∙ ')))

        id_temperature = 'temperature-wrap'
        id_category = 'article-category'
        id_price = 'article-price'
        id_counts = 'article-counts'

        temperature = parse_temperature(self.driver.find_element_by_id(id_temperature).text)
        category = parse_category(self.driver.find_element_by_id(id_category).text)
        price = parse_price(self.driver.find_element_by_id(id_price).text)
        counts = parse_counts(self.driver.find_element_by_id(id_counts).text)
        return temperature, category, price, counts

    def collect(self):
        self.enter()
        notifier = LocationNotifier()
        addresses = notifier.get_all_address()
        for address in addresses:
            time.sleep(1)
            self.search_village(address)
            for idx, link in enumerate(self.get_product_link()):
                self.enter_product_link(link)
                yield self.get_product_information()


for v in ProductDataCollector().collect():
    print(v)

