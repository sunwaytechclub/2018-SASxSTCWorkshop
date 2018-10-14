import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class StockSpider(scrapy.Spider):
    name = "stock"
    start_urls = [
        'https://www.bloomberg.com/quote/MAY:MK'
    ]

    '''
    Called after every request
    This is where your scrapping code should be
    '''
    def parse(self, response):
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True
        browser = webdriver.Firefox(capabilities=cap, firefox_binary="/usr/bin/firefox-nightly")
        browser.get(response.url)
        result = response.xpath('//script[@type="text/javascript"]/text()').extract()

        return {"result": browser.page_source}