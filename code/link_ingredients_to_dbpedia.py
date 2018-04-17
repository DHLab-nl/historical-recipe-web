# coding: utf-8

# This script reads in the ingredients file and tries to find its corresponding
# dbedia page. From that page, it will try to extract the scientific name
# its output serves to query the scientific name against GBIF to get its native
# range

# Marieke.van.Erp@dh.huc.knaw.nl
# 23 March 2018


import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from time import sleep
import spotlight

def dbpedia_links(itempje):
    results_dict = {}
    results_dict['scientific'] = ''
    results_dict['dbpedia_en'] = ''
    results_dict['uri'] = ''
    address = itempje
    sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql/")
    query = u"""SELECT ?object ?dbpedia_en ?uri
            WHERE {
            VALUES ?uri
                {
                %s
                }
                ?uri <http://www.w3.org/2002/07/owl#sameAs> ?dbpedia_en .
                OPTIONAL { ?uri <http://dbpedia.org/ontology/scientificName> ?object . }
                FILTER(regex(str(?dbpedia_en), "http://dbpedia.org/"))
                }
        LIMIT 10""" % (address)
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            try:
                results_dict['scientific'] = result['object']['value']
            except:
                pass
            try:
                results_dict['dbpedia_en'] = result['dbpedia_en']['value']
            except:
                pass
            try:
                results_dict['uri'] = result['uri']['value']
            except:
                pass
    except:
        pass
    return(results_dict)

uniek_lijstje = []
with open("./data/unique_ingredients.csv", 'r') as x:
    for line in x:
        line = line.rstrip()
        elems = line.split(",")
        uniek_lijstje.append(elems[0])


f= open("data/unique_ingredients_with_dbpedia-en-science_WedMorning.tsv","w+")

counter = 1
for item in uniek_lijstje:
    try:
        text = item.rstrip()
        annotations = spotlight.annotate('http://api.dbpedia-spotlight.org/nl/annotate', text, confidence=0.5, support=10)
        spotty = annotations[0]['URI']
        spotty_conf = annotations[0]['similarityScore']
        spotty_support = annotations[0]['support']
        via_spotlight = dbpedia_links("<" + spotty + ">")
    except:
        #'No Resources found in spotlight response: %s' % pydict
        spotty = ""
        via_spotlight['scientific'] = ''
        via_spotlight['dbpedia_en'] = ''
        spotty_conf = ""
        spotty_support = ""
    new_item = item.title()
    new_item = new_item.replace(" ", "_")
    address = "<http://nl.dbpedia.org/resource/" + new_item + ">"
    dus = dbpedia_links(address)
    print(str(counter), item)
    counter = counter +1
    f.write(item + "\t" + dus['uri'] + "\t" + dus['scientific']+  "\t" +  dus['dbpedia_en'] + "\t" + spotty + "\t" + str(spotty_conf) + "\t" + str(spotty_support) + "\t" + via_spotlight['scientific'] + "\t" + via_spotlight['dbpedia_en'] + "\n")
    sleep(2)
