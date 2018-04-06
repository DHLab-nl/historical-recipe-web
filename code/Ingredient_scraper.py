#!/usr/bin/env python

"""
Usage: Ingredient_scraper.py

This script extract information on the ingredients and quantities
from the Allerhande XML data and turns this into a csv.
"""

# author: melvinwevers@gmail.com

from bs4 import BeautifulSoup
import pandas as pd
import glob


file_list = glob.glob("./www.ah.nl/allerhande/recept/**/*/*", recursive=True)


def allerhande_parser(data):
    """Function for extracting ingredients and units from Allerhande xml"""
    dfcols = ['id_', 'data-search-term', 'description-plural',
              'description-plural', 'quantity', 'quantity-unit-singular',
              'quantity-unit-plural', 'additional_info', 'default-label']
    df = pd.DataFrame(columns=dfcols)
    for i in data:
        xml = open(i)
        soup = BeautifulSoup(xml, 'lxml-xml')
        if soup.find('div', class_='container detail') is not None:
            id_ = soup.find('div', class_='container detail').attrs['data-dax-id']
        else:
            id_ = ""
        for data in soup.find_all('ul', class_='list shopping ingredient-selector-list'):
            for a in data.find_all('a'):
                term = a.attrs['data-search-term']
                value1 = a.attrs['data-description-singular']
                value2 = a.attrs['data-description-plural']
                value3 = a.attrs['data-quantity']
                value4 = a.attrs['data-quantity-unit-singular']
                value5 = a.attrs['data-quantity-unit-plural']
                value6 = a.attrs['data-additional-info']
                value7 = a.attrs['data-default-label']
        df = df.append(pd.Series([id_, term, value1, value2, value3, value4, value5, value6, value7], index=dfcols), ignore_index=True)
        df.to_csv("./data/ingredient_list_raw.csv")
    return df


if __name__ == '__main__':
    allerhande_parser(file_list)
