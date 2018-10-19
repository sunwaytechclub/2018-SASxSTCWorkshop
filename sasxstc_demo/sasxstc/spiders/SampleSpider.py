import scrapy


class SampleSpider(scrapy.Spider):
    name = "sample"
    start_urls = [
        'https://sunwaytechclub.github.io/2018-SASxSTCWorkshop/1.html'
    ]

    '''
    Called after every request
    This is where your scrapping code should be
    '''
    def parse(self, response):
        result = response.xpath('//div[@id="d02"]/p[@class="red"]/text()').extract()

        return {"result": result}