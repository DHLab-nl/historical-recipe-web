# Historical Recipe Web
Repo for our paper 'Constructing a Recipe Web from Historical Newspapers'

Authors: Marieke van Erp, Melvin Wevers, Hugo Huurdeman

<img src="figures/workflow.png">


## Code
This directory contains the code used for our experiments.

### Parsing Allerhande Data
We scraped the recipes from the Allerhande website. We used the following scripts to parse and clean this data.

* Allerhande_Parser.py <br>
This script takes html data scraped from Allerhande website and
turns this into a csv file that can be used for further analysis

* CleanSet.ipynb <br>
This notebook details the cleaning steps and describe how we engineered the features.

### Extracting & Classifying Historical recipes
We extracted recipes from four newspapers in the Delpher digitized newspaper collection. Due to copyright restriction, we cannot offer these newspapers in the repo. The KB can be contacted for a license. We, however, added the IDs of the recipes in the dataset.

* Extract_recipes.ipynb <br>
This notebook describes how (1) we extracted the articles from the newspapers using query words. (2) created a clean set of articles after annotating the data created in step 1. We annotated whether the articles were recipes or not.

* Classify_recipes.ipynb & Classify_recipes.py <br>
This notebook and python script show how we trained the classifier and applied the classifier to the newspaper data to increase our set of historical recipes.

### Training Tag classifier
We trained a multilabel (tag) classifier on top of the Allerhande data. We then applied this tag classifier to the historical recipes extracted from the newspapers.

* Classifier-tags.py & classifier_Tags.ipynb


# Models
This directory contains the trained Models

# Figures
Here you can find the images used in the paper.

# TO DO:
* Add list of ingredients derived from AH
* Add final dataset without copyrighted material
