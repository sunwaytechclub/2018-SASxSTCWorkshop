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

        data = pandas.DataFrame(
            {
                "gdp_growth": gdp_growth,
                "infant_mortality": infant_mortality,
                "population_growth": population_growth
            },
            index=country_name
        )

        data = data.dropna(how='any')

        slope, intercept, r_value, p_value, std_err = stats.linregress(data["infant_mortality"].tolist(), data["population_growth"].tolist())

        seaborn.jointplot(x="infant_mortality", y="population_growth", data=data,
                          kind="reg", stat_func=stats.pearsonr)
        # pyplot.legend(
        #     [
        #         "y={0:.1f}x+{1:.1f}".format(slope, intercept),
        #         "Country",
        #         "Confidence Interval"
        #     ], ncol=2, loc='upper left')
        pyplot.annotate("y={0:.1f}x+{1:.1f}".format(slope, intercept), xy=(0.05, 0.95), xycoords='axes fraction')
        pyplot.show()

        # return item
