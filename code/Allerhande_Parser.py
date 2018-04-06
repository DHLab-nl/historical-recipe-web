#!/usr/bin/env python

"""
Usage: Allerhande_Scraper.py

This script takes html data scraped from Allerhande website and
turns this into a csv file that can be used for further analysis
"""

# author: melvinwevers@gmail.com

from bs4 import BeautifulSoup
import pandas as pd
import glob


file_list = glob.glob("./www.ah.nl/allerhande/recept/**/*/*", recursive=True)


def allerhande_parser(data):
    '''
    function to parse webscrape from Allerhande website into to_csv
    '''
    dfcols = ['id_', 'title', 'description', 'course', 'recipe_yield',
              'ingredients', 'calories', 'protein', 'carbohydrates', 'fat',
              'saturated_fat', 'sodium', 'fiber', 'cooking_time', 'rating',
              'review_count', 'recipe_instruction', 'source', 'tags',
              'appliances']
    df = pd.DataFrame(columns=dfcols)
    for i in data:
        xml = open(i)
        soup = BeautifulSoup(xml, 'lxml-xml')
        id_ = soup.find('div', class_='container detail').attrs['data-dax-id']
        title = soup.find("meta", property="twitter:title")['content']
        description = soup.find("meta", property="twitter:description")['content']
        try:
            if soup.find("div", class_="microdata").find(itemprop="recipeCategory").text:
                course = soup.find("div", class_="microdata").find(itemprop="recipeCategory").text
        except AttributeError:
            course = ''
        try:
            if soup.find("div", class_="microdata").find(itemprop="recipeYield").text:
                recipe_yield = soup.find("div", class_="microdata").find(itemprop="recipeYield").text
        except AttributeError:
            recipe_yield = ''
        try:
            if soup.find(itemprop="calories").text:
                calories = soup.find(itemprop="calories").text
        except AttributeError:
            calories = ''
        try:
            if soup.find(itemprop="proteinContent").text:
                protein = soup.find(itemprop="proteinContent").text
        except AttributeError:
            protein = ''
        try:
            if soup.find(itemprop="carbohydrateContent").text:
                carbohydrates = soup.find(itemprop="carbohydrateContent").text
        except AttributeError:
            carbohydrates = ''
        try:
            if soup.find(itemprop="saturatedFatContent").text:
                saturated_fat = soup.find(itemprop="saturatedFatContent").text
        except AttributeError:
            saturated_fat = ''
        try:
            if soup.find(itemprop="fatContent").text:
                fat = soup.find(itemprop="fatContent").text
        except AttributeError:
            fat = ''
        try:
            if soup.find(itemprop="sodiumContent").text:
                sodium = soup.find(itemprop="sodiumContent").text
        except AttributeError:
            sodium = ''
        try:
            if soup.find(itemprop="fiberContent").text:
                fiber = soup.find(itemprop="fiberContent").text
        except AttributeError:
            fiber = ''
        try:
            if soup.find("li", class_="cooking-time").find('li').text:
                cooking_time = soup.find("li", class_="cooking-time").find('li').text
        except AttributeError:
            cooking_time = ''

        try:
            if soup.find(itemprop="ratingValue").text:
                rating = soup.find(itemprop="ratingValue").text
        except AttributeError:
            rating = ''
        try:
            if soup.find(itemprop="reviewCount").text:
                review_count = soup.find(itemprop="reviewCount").text
        except AttributeError:
            review_count = ''
        try:
            if soup.find(itemprop="recipeInstructions").find('li').text:
                recipe_instruction = soup.find(itemprop="recipeInstructions").find('li').text
            elif soup.find(itemprop="recipeInstructions").find('p').text:
                recipe_instruction = soup.find(itemprop="recipeInstructions").find_all('p')[-1].get_text()
        except AttributeError:
            recipe_instruction = ''
        try:
            if soup.find("section", {"class": "source"}).find('div').text:
                source = soup.find("section", {"class": "source"}).find('div').text
        except AttributeError:
            source = ''
        ingredients = {}
        for data in soup.find_all('ul', class_='list shopping ingredient-selector-list'):
            for a in data.find_all('a'):
                product = a.attrs['data-search-term']
                value = a.attrs['data-quantity'] + ' ' + a.attrs['data-quantity-unit-singular'] + '(' + a.attrs['data-additional-info'] + ')'
                ingredients[product] = value
        tags = []
        uls = soup.find_all("ul", {"class": "tags"})
        for ul in uls[:1]:
            for li in ul.findAll('li'):
                tags.append(li.text)
        appliances = []
        uls = soup.find_all("ul", {"class": "list kitchenappliances"})
        for ul in uls:
            for li in ul.findAll('li'):
                appliances.append(li.text)
        df = df.append(pd.Series([id_, title, description, course,
                                  recipe_yield, ingredients, calories, protein,
                                  carbohydrates, fat, saturated_fat, sodium,
                                  fiber, cooking_time, rating, review_count,
                                  recipe_instruction, source, tags,
                                  appliances], index=dfcols), ignore_index=True)
        df.to_csv('allerhande_recepten.csv')
    return df


if __name__ == '__main__':
    allerhande_parser()
