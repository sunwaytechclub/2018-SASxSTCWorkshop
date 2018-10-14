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

| Time |              Agenda              |
|:----:|:--------------------------------:|
| 1330 |       Install requirement        |
| 1340 |       Basic Web Scrapping        |
| 1415 | Scrape Bursamktplc with Selenium |
| 1445 |        Panda + Matplotlib        |
| 1620 |               End                |

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