# This folder contains the produced datasets

## recipe_web.pkl
This pickle contains a dataset of 27,411 recipes that we extracted from the historical newspapers and enriched with additional information. <br>
<br>
The columns in the dataframe dataframe are:
* __title__: name of the newspaper
* __date__: publication date of the recipe
* __doc_url__: url to the actual file on the newspaper repository Delpher
* __h__: the height of the article
* __w__: the width of the article
* __ocr_score__: indicator of ocr quality
* __ingredients__: list of ingredients extracted from the recipe
* __quant__: quantities extracted from the recipe
* __tags__: predicted tags for the recipes using the trained tag classifier


## TO DO:
The quantity list needs to map onto the ingredient list. <br>
Ingredients without quantities are not represented by an empty file in the quantity list now.
