# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas
import seaborn
from matplotlib import pyplot
from pprint import pprint
from scipy import stats


class SasxstcPipeline(object):
    def process_item(self, item, spider):
        results = item["results"]
        country_name = []
        population_growth = []
        gdp_growth = []

        for country_code in list(results.keys()):

            country_name.append(results[country_code]["name"])
            population_growth.append(float(results[country_code]["population_growth_rate"]))
            try:
                gdp_growth.append(float(results[country_code]["gdp_growth_rate"]))
            except KeyError:
                gdp_growth.append(None)

        data = pandas.DataFrame(
            {
                "gdp_growth": gdp_growth,
                "population_growth": population_growth
            },
            index=country_name
        )

        data.dropna(how='any')

        def r(x, y):
            r = stats.pearsonr(x, y)[0]
            r2 = stats.pearsonr(x, y)[0] ** 2
            return (r, r2)

        # seaborn.regplot(x="gdp_growth", y="population_growth", data=data)
        seaborn.jointplot(x="gdp_growth", y="population_growth", data=data, kind="reg", stat_func=r)
        pyplot.show()

        # return item
