#!/usr/bin/python
#coding=utf-8

import scrapy
import re
import datetime
from .meal import Meal
from .mealdate import MealDate
from .db import DB

class Wueins(scrapy.Spider):
    name = 'wueins'
    start_urls = ['https://www.studentenwerk-dresden.de/mensen/speiseplan/mensa-wueins.html']

    def parse(self, response):
        tables = response.xpath('//div[@id="spalterechtsnebenmenue"]/table').css('.speiseplan')
        db = DB()
        catering_id = 0
        for t in tables:
            title = t.xpath('thead/tr/th').css('.text::text').extract()

            # Skip action menu
            if len(t.xpath('@id').extract()) > 0:
                continue

            # get date text
            date_name = "19700101"
            format_str = "%Y%m%d"
            date_obj = datetime.datetime.strptime(date_name, format_str)
            if len(title):
                date_name = title[0]
                # Convert date_name to date object
                date_string = date_name.split(',')
                if len(date_string) > 1:
                    date_obj = self.create_date_from_string(date_string[1])

            meals = t.xpath('tbody/tr')
            mealdate_id = int(date_obj.strftime("%Y%m%d"))
            meal_id = 0
            md = MealDate(catering_id, mealdate_id, date_name)
            md.save(db)
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
                # m.save(db)

                meal_id += 1
            mealdate_id += 1

    def create_date_from_string(self, date_string):
        strings = date_string.strip().split(' ')
        format_str = "%Y%m%d"
        date_obj = datetime.datetime.strptime("19700101", format_str)
        if len(strings) == 3:
            day = strings[0].replace('.', '').replace(' ', '')
            month = self.get_month_number(strings[1].replace(' ', ''))
            year = strings[2].replace(' ', '')
            date_str = "{0}{1}{2}".format(year, month, day)
            date_obj = datetime.datetime.strptime(date_str, format_str)

        return date_obj

    def get_month_number(self, month_name):
        month_names = {"Januar": "01",
                       "Februar": "02",
                       "März": "03",
                       "April": "04",
                       "Mai": "05",
                       "Juni": "06",
                       "July": "07",
                       "August": "08",
                       "September": "09",
                       "Oktober": "10",
                       "November": "11",
                       "Dezember": "12"}

        if month_name in month_names:
            return month_names[month_name]

        return "00"
