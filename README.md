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
| 1330 |       Ice Breaking        |
| 1333 |       Introduce TAs       |
| 1334 |    Install requirement    |
| 1350 |    Basic Web Scrapping    |
| 1415 | Scrape CIA world factbook |
| 1445 |    Panda + Matplotlib     |
| 1620 |            End            |

## Slides

[Google Slides](https://docs.google.com/presentation/d/1zm3oYZ_UbkVHQ2HZ5kklCRn90eLR_NYNHRstOSOKncA/edit?usp=sharing)

## Workshop

1. Install all the requirements before start

    ```bash
    $ pip install -r ./requirements.txt
    ```

    OR

    ```bash
    $ python -m pip install -r ./requirements.txt
    ```

1. Error (Windows)
    
    **Lack of TK**

    ```bash
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/local/lib/python3.6/site-packages/matplotlib/pyplot.py", line 115, in <module>
        _backend_mod, new_figure_manager, draw_if_interactive, _show = pylab_setup()
      File "/usr/local/lib/python3.6/site-packages/matplotlib/backends/__init__.py", line 32, in pylab_setup
        globals(),locals(),[backend_name],0)
      File "/usr/local/lib/python3.6/site-packages/matplotlib/backends/backend_tkagg.py", line 6, in <module>
        from six.moves import tkinter as Tk
      File "/usr/local/lib/python3.6/site-packages/six.py", line 92, in __get__
        result = self._resolve()
      File "/usr/local/lib/python3.6/site-packages/six.py", line 115, in _resolve
        return _import_module(self.mod)
      File "/usr/local/lib/python3.6/site-packages/six.py", line 82, in _import_module
        __import__(name)
      File "/usr/local/lib/python3.6/tkinter/__init__.py", line 36, in <module>
        import _tkinter # If this fails your Python may not be configured for Tk
    ModuleNotFoundError: No module named '_tkinter'
    ```

    Solution: Reinstall python and check TK modules

    **Microsoft Visual C++ 14.0**

    ```bash
    running build_ext
    building 'twisted.test.raiser' extension
    error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
    ```

    Solution: 

    1. Manually download twisted from [here](https://www.lfd.uci.edu/%7Egohlke/pythonlibs/)

    1. Run

    ```bash
    $ pip install Twisted‑18.9.0‑cp37‑cp37m‑win32.whl
    ```

    **Lack of pywin32**

    ```bash
    ModuleNotFoundError: No module named 'pywin32'
    ```

    Solution:

    ```bash
    $ pip install pywin32
    ```

    OR

    ```bash
    $ pip install pypiwin32
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
            meta["links"]["Infant mortality rate:"],
            callback=self.parse_infant_mortality,
            meta=meta
        )

    def parse_infant_mortality(self, response):
        meta = response.meta
        results = meta["results"]

        rows = response.xpath('//div[@class="wfb-text-box"]//table[@id="rankOrder"]/tbody/tr')
        for index, row in enumerate(rows):
            if not row.xpath('@class').extract_first() == 'rankHeading':
                id = row.xpath('@id').extract_first()
                infant_mortality_rate = row.xpath('td[3]/text()').extract_first()
                results[id]["infant_mortality_rate"] = infant_mortality_rate

        return results
    ```

1. Getting error? 

    ```bash
    Traceback (most recent call last):
      File "/home/gaara/.virtualenvs/sasxstc/lib/python3.7/site-packages/twisted/internet/defer.py", line 654, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/gaara/Desktop/2018-SASxSTCWorkshop/sasxstc/sasxstc/spiders/FactbookSpider.py", line 60, in parse_gdp
        results[id]["infant_mortality_rate"] = infant_mortality_rate
    KeyError: 'kv'
    ```

    Surround with try and except 

    ```python
    try:
        results[id]["infant_mortality_rate"] = infant_mortality_rate
    except KeyError:
        pass
    ```

1. Now you have the data of factbook with you! 

1. However, before we move forward, let's make use of the pipelines

    Add a field to `projectdir/sasxstc/sasxstc/items.py`
    ```python
    class SasxstcItem(scrapy.Item):
        # define the fields for your item here like:
        results = scrapy.Field()
    ```

    Uncomment the following line in `projectdir/sasxstc/sasxstc/settings.py`
    ```python
    # ITEM_PIPELINES = {
    #    'sasxstc.pipelines.SasxstcPipeline': 300,
    #}
    ```

    Import the item in `projectdir/sasxstc/sasxstc/spiders/FactbookSpider.py`
    ```python
    from sasxstc.items import SasxstcItem
    ```

    Change the last line of `projectdir/sasxstc/sasxstc/spiders/FactbookSpider.py`
    ```python
    # return results
    item = SasxstcItem()
    item["results"] = results
    return item
    ```

1. You are good to go now!

### Analytics

1. Go to `projectdir/sasxstc/sasxstc/pipelines.py`

1. Add imports

    ```python
    import pandas
    import seaborn
    from matplotlib import pyplot
    from pprint import pprint
    from scipy import stats
    ```

1. Seperate results into different list

    ```python
    results = item["results"]
        country_name = []
        population_growth = []
        infant_mortality = []
        gdp_growth = []

        for country_code in list(results.keys()):

            country_name.append(results[country_code]["name"])

            try:
                population_growth.append(float(results[country_code]["population_growth_rate"]))
            except KeyError:
                population_growth.append(None)

            try:
                infant_mortality.append(float(results[country_code]["infant_mortality_rate"]))
            except KeyError:
                infant_mortality.append(None)

            try:
                gdp_growth.append(float(results[country_code]["gdp_growth_rate"]))
            except KeyError:
                gdp_growth.append(None)
    ```

1. Put data into Panda dataframe

    ```python
    data = pandas.DataFrame(
            {
                "gdp_growth": gdp_growth,
                "infant_mortality": infant_mortality,
                "population_growth": population_growth
            },
            index=country_name
        )

    pprint(data)
    ```

1. Run it and see how the data looks like

1. Drop the row with empty field

    ```python
    data = data.dropna(how='any')
    pprint(data)
    ```

1. Plot the graph

    ```python
    seaborn.jointplot(x="infant_mortality", y="population_growth", data=data, kind="reg")

    pyplot.show()
    ```

1. Run it!

1. Now, add R and P value?

    ```python
    seaborn.jointplot(x="infant_mortality", y="population_growth", data=data,
                      kind="reg", stat_func=stats.pearsonr)
    ```

1. Add the equation of regression line

    ```python
    slope, intercept, r_value, p_value, std_err = stats.linregress(data["infant_mortality"].tolist(), data["population_growth"].tolist())

    seaborn.jointplot(x="infant_mortality", y="population_growth", data=data,
                      kind="reg", stat_func=stats.pearsonr)
    pyplot.annotate("y={0:.1f}x+{1:.1f}".format(slope, intercept), xy=(0.05, 0.95), xycoords='axes fraction')
    pyplot.show()
    ```

1. And, you are done!