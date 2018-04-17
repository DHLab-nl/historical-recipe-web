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

## DBpedia links  
unique\_ingredients\_with\_dbpedia-en-science\_links.tsv contains the allerhande ingredients, with links added via stringmatch and DBpedia spotlight to the Dutch DBpedia, and where available also to the English DBpedia and the scientific name. 

The columns denote:   
* __Ingredient__: Ingredient name  
* __DBpedia\_link\_via\_stringmatch__: Link to Dutch DBpedia resource via string match   
* __Judgment\_stringmatch__: Judgment by annotator on correctness of link (1 is correct, 0 is incorrect)  
* __Scientific\_name\_via\_stringmatch__:  scientific name as queried from _dbo:scientific_name_  
* __dbpedia-en\_via\_stringmatch__: Link to English DBpedia    	 
* __DBpedia\_via\_spotlight__:  Link to Dutch DBpedia via DBpedia spotlight  	  
* __Judgment\_spotlight__:  Judgment by annotator on correctness of link (1 is correct, 0 is incorrect)   
* __spotlight\_conf__:  additional information provided by Spotlight on the confidence of the link decision  
* __spotlight\_support__:  additional information provided by Spotlight on the support for the link decision 	  
* __Scientific\_name\_via\_spotlight__: scientific name as queried from _dbo:scientificName_   
* __dbpedia-en\_via\_spotlight__:	  Link to English DBpedia    	 

## GBIF links 


## TO DO:
The quantity list needs to map onto the ingredient list. <br>
Ingredients without quantities are not represented by an empty file in the quantity list now.
