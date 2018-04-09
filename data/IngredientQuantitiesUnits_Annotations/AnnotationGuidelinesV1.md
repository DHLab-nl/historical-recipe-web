Ingredient and quantities annotation guidelines
===============================

Author: Marieke van Erp  
Date: 30 March 2018

Introduction
-------
To assess the quality of the ingredient and quantities/units extraction, correct ingredient and quantities/unit mentions are to be annotated in the evaluation dataset. 

Annotation Tool
------------
The [Recogito](https://recogito.pelagios.org/) annotation tool is used for the annotations process. This tool was designed to annotate geographical locations, persons and events, but these categories can easily be repurpsed to quantities/units, ingredients, and ingredients with OCR errors. The interface of the Recogito tool is simple, doesn't require separate installations and allows for collaborative editing. 


To do: discuss batch document upload and sharing with Recogito developers 

Ingredient annotation
-------
Each ingredient that does not contain any OCR errors is to be marked in blue (using Recogito's "Person" class). For example: 

kipfilet -> ingredient  
kipf>1et -> not to be marked as an ingredient (see Ingredients with OCR errors)

Ingredients that contain information about their state, e.g. gemalen komijn (ground cumin) or fijngehakte peterselie (chopped parsley), only annotate the ingredient, not its shape e.g. "<span style="color:blue">komijn</span>" and "<span style="color:blue">parsley</span>". 

Concatenated ingredients such as "peper en zout" (pepper and salt) are to be annotated separately, i.e. "<span style="color:blue">peper</span>" and "<span style="color:blue">salt</span>". 

For contracted ingredients such as "kippemaagjes en -levertjes" (chicken stomachs or livers) annotate as a single ingredient, thus "<span style="color:blue">kippemaagjes en -levertjes</span>".

Ingredients with OCR errors 
---------
If you recognise an ingredient in a string, but the string is affected by one or more OCR errors, please mark this ingredient in <span style="color:pink">pink</span> (the Recogito "Event" class) to denote it as an ingredient with OCR errors. 

For example:   
<span style="color:pink">wyn</span> (correct OCR would have been: "wijn")   
<span style="color:pink">nºtemuskaat</span> (correct OCR would have been: "nootmuskaat")  
<span style="color:pink">vanlillpwafeltjes</span> (correct OCR would have been: "vanillewafeltjes")

OCR errors in tokens not denoting ingredients are to be ignored. 


Quantity and unit annotation
---------------

Quantities and units are to be annotated in <span style="color:green">green</span> (the Recogito "Place" class). 

For example:  
<span style="color:green">circa 50 gram</span>   
<span style="color:green">400 grams</span>  
<span style="color:green">250 - 300 grams</span>  
<span style="color:green">2 eetlepels</span> (2 tablespoons) one annotation   
<span style="color:green">3 blaadjes</span> (3 leaves) one annotation  
<span style="color:green">1</span> (as in 1 onion)

In strings such as "1 kleine ui" (1 small onion), "1" is to be marked as a quantity and "ui" as ingredient.    

Plurals and names of dishes or mixes
-----------
Plural and singular forms of ingredients are to be annotated both e.g. if both "kiwi" and "kiwi's" (kiwis) are mentioned in the article, please annotate both. 

Do not annotate names of dishes such as aardbeienkwarktaart (strawberry cheesecake) or resulting mixes of a previous step in the recipe, for example the resulting "gehaktmengsel" (minced meat mixture) from putting together minced meat and herbs. Likewise, if the ingredients list states "carrots", "onions" and "courgette" separately, and a bit further on the recipe mentions something like "add the vegetables" do not annotate "vegetables".  

Tips & Tricks 
-----------

* be careful when Recogito suggest to annotate further occurrences of a string automatically for you, especially short strings such as "ui" (onion) and "ei" (egg) can yield undesired results
* each ingredient mention only needs to be annotated once, however, they can be annotated multiple times if you want to be sure that none are forgotten 
* using the "Quick" annotation mode in Recogito is handy to speed up the annotation process 
 



