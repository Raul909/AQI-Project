# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:34:41 2019

@author: krish.naik
"""
import os
import time
import requests
import sys


def retrieve_html(start_year=2013, end_year=2019):
    for year in range(start_year, end_year):
        for month in range(1, 13):
            url = f'https://en.tutiempo.net/climate/{month:02d}-{year}/ws-421820.html'
            texts = requests.get(url, timeout=20)
            text_utf = texts.text.encode('utf-8')

            if not os.path.exists(f"Data/Html_Data/{year}"):
                os.makedirs(f"Data/Html_Data/{year}")
            with open(f"Data/Html_Data/{year}/{month}.html", "wb") as output:
                output.write(text_utf)

        sys.stdout.flush()


if __name__ == "__main__":
    start_time = time.time()
    retrieve_html()
    stop_time = time.time()
    print(f"Time taken {stop_time - start_time}")
