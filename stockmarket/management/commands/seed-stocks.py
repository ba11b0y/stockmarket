import csv
import io
import os
from datetime import datetime
from os import listdir
from zipfile import ZipFile

import requests
from django.core.management.base import BaseCommand
from requestium import Session
from stockmarket.models import Stock
import DBMS_PROJECT.settings as settings

MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

class Command(BaseCommand):
    help = "Use to seed stocks"

    def add_arguments(self, parser):
        # parser.add_argument('only', nargs=1, type=str)
        pass

    def handle(self, *args, **options):
        print("Cleaning old stocks")
        # self.clear()
        print("Beginning to seed")
        import pdb; pdb.set_trace()
        self.fetch_latest_bhavcopy()
        stock_data = self.read_from_file()
        self.seed(stock_data)

    def fetch_latest_bhavcopy(self):
        nse_url = "https://www.nseindia.com/products/content/equities/equities/homepage_eq.htm"
        s = Session(webdriver_path='./chromedriver',
                browser='chrome',
                default_timeout=15,
                webdriver_options={'arguments': ['headless']})
        s.driver.get(nse_url)
        link = s.driver.ensure_element_by_link_text('Bhavcopy file (csv)').get_attribute('href')
        s.driver.close()
        r = requests.get(link)  
        open('bhav.csv.zip', 'wb').write(r.content)

    def clear(self):
        return None
    def read_from_file(self):
        stock_data = []
        _file = os.path.join(settings.BASE_DIR, 'bhav.csv.zip')
        with ZipFile(_file) as zipfile:
            zipfile.extractall(path=settings.BASE_DIR)
        csv_file = os.path.join(settings.BASE_DIR, find_csv_filenames(settings.BASE_DIR)[0])
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["SERIES"] == "EQ":
                    stock_data.append({"tick": row["SYMBOL"], "prevclose": row["PREVCLOSE"]})
        return stock_data
        
    def seed(self, stock_data):
        if Stock.objects.count() == 0:
            objs = (Stock(name=s["tick"], ltp=s["prevclose"]) for s in stock_data)
            Stock.objects.bulk_create(objs)
        else:
            objs = (Stock(name=s["tick"], ltp=s["prevclose"]) for s in stock_data)
            Stock.objects.bulk_update(objs, ["prevclose"])
