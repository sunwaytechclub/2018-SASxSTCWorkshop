# 2018-SASxSTCWorkshop

## Agenda

| Time |          Agenda           |
|:----:|:-------------------------:|
| 0930 |    Registration start     |
| 1020 |          Opening          |
| 1030 | Analytic Talk by Fusionex |
| 1200 |           Q & A           |
| 1230 |           Lunch           |
| 1330 |      Workshop start       |
| 1620 |       Ending Speech       |
| 1630 |            End            |

**Workshop Agenda**

| Time |          Agenda           |
|:----:|:-------------------------:|
| 1330 |    Install requirement    |
| 1340 |    Basic Web Scrapping    |
| 1415 | Scrape CIA world factbook |
| 1445 |    Panda + Matplotlib     |
| 1620 |            End            |

## Slides

[Google Slides]()

## Workshop

1. Install all the requirements before start

    ```bash
    $ pip install -r ./requirements.txt
    ```

    OR

    ```bash
    $ python -m pip install -r ./requirements.txt
    ```

### Scrapping Workshop

1. First, create a scrapy project

    ```bash
    $ scrapy startproject sasxstc
    ```

1. We will start by scrapping this [website](https://sunwaytechclub.github.io/2018-SASxSTCWorkshop/1.html)

1. Create a new file in `projectdir/sasxstc/sasxstc/spiders/SampleSpider.py`

1. Insert below boilerplate code into `SampleSpider.py`

    ```python
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
            result = response.body
            return {"result": result}
    ```

1. Run the spider

    ```bash
    $ scrapy crawl sample
    ```

1. If you get the following error:

    ```bash
      File "/home/gaara/.virtualenvs/sasxstc/lib/python3.7/site-packages/twisted/conch/manhole.py", line 154
        def write(self, data, async=False):
                                  ^
    SyntaxError: invalid syntax
    ``` 

    *run* 

    ```bash
    $ pip install git+https://github.com/twisted/twisted.git@trunk
    ```

1. Xpath basic

    ```python
    # Extract every html tag
    result = response.xpath('//html').extract()
    ```

    ```python
    # Extract the body tag which follow by html
    result = response.xpath('//html/body').extract()
    ```

    ```python
    # Extract every body tag
    result = response.xpath('//body').extract()
    ```

    ```python
    # Extract the p tag that follow by div, body and html
    result = response.xpath('//html/body/div/p').extract()
    ```

    ```python
    # Extract the text within every p tag
    result = response.xpath('//p/text()').extract()
    ```

1. Xpath with id and class

    ```python
    # Extract every element within div with id of 'd01'
    result = response.xpath('//div[@id="d01"]').extract()
    ```

    ```python
    # Extract all the text with class blue
    result = response.xpath('//p[@class="blue"]/text()').extract()
    ```

    ```python
    # Extract the word SAS
    result = response.xpath('//div[@id="d02"]/p[@class="red"]/text()').extract()
    ```

### Scrapping CIA factbook

CIA is Central Intelligence Agency. Various data can be found in CIA factbook, such as country GDP, population growth rate, etc. The list of data can be found in [here](https://www.cia.gov/library/publications/the-world-factbook/rankorder/rankorderguide.html).

1. So, first, visit this [url](https://www.cia.gov/library/publications/the-world-factbook/rankorder/rankorderguide.html) and observe the website. 

1. Let's create an empty spider `FactbookSpider.py`
    
    ```python
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
            pass
    ```

1. Time to get the link

    ```python
    links = response.xpath('//body//div[@id="profileguide"]/div[@class="answer"]//a')
    for index, link in enumerate(links):
        text = link.xpath('text()').extract_first()
        link = link.xpath('@href').extract_first()
        print(text)
        print(link)
    ```

1. Now, join the url

    ```python
    link = response.urljoin(link.xpath('@href').extract_first())
    ```

1. Put the links into results object
    
    ```python
    links = response.xpath('//body//div[@id="profileguide"]/div[@class="answer"]//a')
    results = {}
    for index, link in enumerate(links):
        text = link.xpath('text()').extract_first()
        link = response.urljoin(link.xpath('@href').extract_first())
        results[text] = link

    pprint(results)
    ```

1. Crawl into one of the link

    ```python
    def parse(self, response):
        links = response.xpath('//body//div[@id="profileguide"]/div[@class="answer"]//a')
        results = {}
        for index, link in enumerate(links):
            text = link.xpath('text()').extract_first()
            link = response.urljoin(link.xpath('@href').extract_first())
            results[text] = link

        yield scrapy.Request(
            results["Population growth rate:"],
            callback=self.parse_population,
            meta={"links": results}
        )

    def parse_population(self, response):
        meta = response.meta
        pprint(meta)
    ```

1. Scrape the row and store into results

    ```python
    rows = response.xpath('//div[@class="wfb-text-box"]//table[@id="rankOrder"]/tbody/tr')
    results = {}
    for index, row in enumerate(rows):
        if not row.xpath('@class').extract_first() == "rankHeading":
            id = row.xpath('@id').extract_first()
            name = row.xpath('td[@class="region"]//text()').extract_first()
            population_growth = row.xpath('td[3]/text()').extract_first()
            print(id + " " + name + " " + population_growth)
            results[id] = {
                "name": name,
                "population_growth_rate": population_growth
            }
    ```

1. Do the same to extract gdp growth rate

    ```python
    def parse_population(self, response):
        meta = response.meta
        rows = response.xpath('//div[@class="wfb-text-box"]//table[@id="rankOrder"]/tbody/tr')
        results = {}
        for index, row in enumerate(rows):
            if not row.xpath('@class').extract_first() == "rankHeading":
                id = row.xpath('@id').extract_first()
                name = row.xpath('td[@class="region"]//text()').extract_first()
                population_growth = row.xpath('td[3]/text()').extract_first()
                results[id] = {
                    "name": name,
                    "population_growth_rate": population_growth
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
                gdp_growth = row.xpath('td[3]/text()').extract_first()
                results[id]["gdp_growth_rate"] = gdp_growth

        return results
    ```

1. Getting error? 

    ```bash
    Traceback (most recent call last):
      File "/home/gaara/.virtualenvs/sasxstc/lib/python3.7/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/gaara/Desktop/2018-SASxSTCWorkshop/sasxstc/sasxstc/spiders/FactbookSpider.py", line 60, in parse_gdp
        results[id]["gdp_growth_rate"] = gdp_growth
    KeyError: 'kv'
    ```

    Surround with try and except 

    ```python
    try:
        results[id]["gdp_growth_rate"] = gdp_growth
    except KeyError:
        pass
    ```

1. Now you have the data of factbook with you! 

