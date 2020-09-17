Python GUI application that lists cocktail ingredients, and based on your selection offers you recipes based on content @ www.cubadrinks.com

The scapeData.py script scrapes the data, and stores the raw BeautifoulSoup html text, and also the extract recipe items as a dict saved in the json file.

The recipeApp.py script spawns the Tkinter GUI, and with some simple sorting / selection functions generates the data output.