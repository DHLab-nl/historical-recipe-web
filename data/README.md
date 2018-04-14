# This folder contains the produced datasets

## recipe_web.pkl
This pickle contains a dataset of 27,411 recipes that we extracted from the historical newspapers and enriched with additional information. <br>
The columns in the dataframe dataframe are:
* title: name of the newspaper
* date: publication date of the recipe
* doc_url: url to the actual file on the newspaper repository Delpher
* h: the height of the article
* w: the width of the article
* ocr_score: indicator of ocr quality
* ingredients: list of ingredients extracted from the recipe
* quant: quantities extracted from the recipe
* tags: predicted tags for the recipes using the trained tag classifier


## TO DO:
The quantity list needs to map onto the ingredient list. <br>
Ingredients without quantities are not represented by an empty file in the quantity list now.
