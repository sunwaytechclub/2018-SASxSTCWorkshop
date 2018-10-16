from pprint import pprint
import scrapy


class FactbookSpider(scrapy.Spider):
    name = "factbook"
    start_urls = [
        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/rankorderguide.html'
    ]

    '''
    Called after every request
    This is where your scrapping code should be
    '''

    def parse(self, response):
        links = response.xpath('//body//div[@id="profileguide"]/div[@class="answer"]//a')
        results = {}
        for index, link in enumerate(links):
            results[link.xpath('text()').extract_first()] = response.urljoin(link.xpath('@href').extract_first())

        yield scrapy.Request(
            results["Population growth rate:"],
            callback=self.parse_population,
            meta={"links": results}
        )

    def parse_population(self, response):
        meta = response.meta
        rows = response.xpath('//div[@class="wfb-text-box"]//table[@id="rankOrder"]/tbody/tr')
        results = {}
        for index, row in enumerate(rows):
            if not row.xpath('@class').extract_first() == "rankHeading":
                results[row.xpath('@id').extract_first()] = {
                    "name": row.xpath('td[@class="region"]//text()').extract_first(),
                    "population_growth_rate": row.xpath('td[3]/text()').extract_first()
                }
        meta["results"] = results
        yield scrapy.Request(
            meta["links"]["GDP - real growth rate:"],
            callback=self.parse_gdp,
            meta=meta
        )

    def parse_gdp(self, response):
        meta = response.meta
        results = meta["results"]

        rows = response.xpath('//div[@class="wfb-text-box"]//table[@id="rankOrder"]/tbody/tr')
        for index, row in enumerate(rows):
            if not row.xpath('@class').extract_first() == 'rankHeading':
                id = row.xpath('@id').extract_first()
                try:
                    results[id]["gdp_growth_rate"] = row.xpath('td[3]/text()').extract_first()
                except KeyError:
                    results[id] = {
                        "name": row.xpath('td[@class="region"]//text()').extract_first(),
                        "gdp_growth_rate": row.xpath('td[3]/text()').extract_first()
                    }

        return results
