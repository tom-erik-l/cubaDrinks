Python GUI application that lists cocktail ingredients, and based on your selection offers you recipes based on content @ www.cubadrinks.com

The scapeData.py script scrapes the data, and stores the raw BeautifoulSoup html text, and also the extract recipe items as a dict saved in the json file.

The recipeApp.py script spawns the Tkinter GUI, and with some simple sorting / selection functions generates the data output.

TO-DO:
Port it to a web-app on your own server

Implemented Favourites listbox
Save Favourites into a txt file, similarly to ingredients to retain the state
Implement actions for adding / removing to favourites list box via Mouse right click menu 
If a favourite is possible with the given ingredients, highlight it in a green colour
Implement a disliked list in a .txt file, and stop these from appearing the possible cocktail lists
Implement a right click action for adding to the disliked list 
