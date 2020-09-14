import requests #to make HTTP URL requests
import urllib.request
import time #to get the time.sleep function
from bs4 import BeautifulSoup #to extract data from html files
import shelve #to save data to a shelve (kinda like matlab save workspace)
import logging #to do logging info and debug statements
import re #regular expressions
import json
import os.path
import traceback

def loggingConfig():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

loggingConfig()

htmlFile = "cubaDrinks.html"
try:
    logging.debug("try to open existing: " + htmlFile)
    if not os.path.exists(htmlFile):
        raise Exception

    with open(htmlFile, "r", encoding='utf-8') as file:
        soup = BeautifulSoup(file, "html.parser", from_encoding='utf8')

    logging.debug(htmlFile + " closed again")
    print("*** Pulled from" + htmlFile + " ***")

# if it doesn't exist, create the data object again
except Exception:
    traceback.print_exc()
    print("*** Pulling data from URL *** ")
    url = "https://cubavodka.com/cocktails"
    # Needed to add a different user agent, since default python one seems blocked?
    # https://stackoverflow.com/questions/56101612/python-requests-http-response-406
    response = requests.get(url, headers={"User-Agent": "XY"})
    # print(response)
    soup = BeautifulSoup(response.text, "html.parser", from_encoding='utf8')

    with open(htmlFile, "w", encoding='utf-8') as file:
        file.write(str(soup))

# Prepare an empty dictionary for all the recipies
recipeDict = {}
imgDir = "images"
if not os.path.exists("./" + imgDir):
    os.mkdir(imgDir)


# Find all the different cocktails in the dataset
for tag in soup.body.find_all(class_=re.compile("cocktail-item")):
    # print(str(tag) + "\n")
    drinkImgUrl = tag["data-largeimg"]
    drinkInstructions = cleanhtml(tag["data-info"])
    drinkName = tag.find("h3", attrs={"itemprop": True}).string
    recipe = tag.find(class_=re.compile("ingredients-wrap"))
    # print(recipe)

    imgPath = imgDir + "/" + drinkName + ".png"
    if not os.path.exists(imgPath):
        urllib.request.urlretrieve(drinkImgUrl, imgPath)

    # Put the drink into the recipeDict!
    recipeDict[str(drinkName)] = {"ingredients": {}, "image": imgPath}

    for ingredient in recipe.find_all("li", attrs={"itemprop": True}):
        # print(ingredient)

        # Ingredients with an amount
        try:
            ingredientName = ingredient.contents[1]
            # print(ingredientName)
            amount = ingredient.span.string
            # print(amount)
        except IndexError:
            pass

        # Ingredientwithout an amount
        try:
            if not ingredient.string == None:
                ingredientName = ingredient.string
                # print(ingredientName)
                amount = " "
        except IndexError:
            pass

        # Put it all into the dict!
        recipeDict[str(drinkName)]["ingredients"][ingredientName] = amount
        recipeDict[str(drinkName)]["instructions"] = drinkInstructions

with open("drinkRecipes.json","w", encoding='utf8') as json_file:
    json.dump(recipeDict, json_file, indent=4, sort_keys=True, ensure_ascii=False)


