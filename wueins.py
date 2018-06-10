#!/usr/bin/python
#coding=utf-8

import scrapy
import re
from .meal import Meal
from .db import DB

class Wueins(scrapy.Spider):
    name = 'wueins'
    start_urls = ['https://www.studentenwerk-dresden.de/mensen/speiseplan/mensa-wueins.html']

    def parse(self, response):
        tables = response.xpath('//div[@id="spalterechtsnebenmenue"]/table').css('.speiseplan')
        db = DB()
        catering_id = 0
        mealdate_id = 0
        for t in tables:
            title = t.xpath('thead/tr/th').css('.text::text').extract()
            print(title[0])
            meals = t.xpath('tbody/tr')
            meal_id = 0
            for m in meals:
                meal_name = m.xpath('td').css('.text').xpath('a/text()').extract()
                meal_price = m.xpath('td').css('.preise').xpath('a/text()').extract()

                name = "kein Anbegot"
                prices = ["0", "0"]
                if len(meal_price):
                    name = meal_name[0]
                    prices = meal_price[0].split("/")
                    for i in range(len(prices)):
                        match = re.search('\d+,\d+', prices[i])
                        prices[i] = match.group(0) + "€"

                m = Meal(catering_id, mealdate_id, meal_id, name, str(prices[0]), str(prices[1]))
                print(m)
                m.save(db)

                meal_id += 1
            mealdate_id += 1
