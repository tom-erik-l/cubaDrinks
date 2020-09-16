import json
import traceback
from tkinter import *
from PIL import Image # pillow module
from PIL import ImageTk # pillow module
import math
import logging

def loggingConfig():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")


class DrinksApp:
    def __init__(self, parent):
        self.myParent = parent  ### (7) remember my parent, the root
        self.Ingredients(parent)
        self.Drinks(parent)
        self.Drinks1Missing(parent)
        self.displayDrink = self.DisplayDrink(parent)


    class ScrollableListBox:
        def __init__(self,**kwargs):
            if "tkParent" in kwargs:
                tkParent = kwargs["tkParent"]
            if "labelText" in kwargs:
                labelText = kwargs["labelText"]
            if "selectmode" in kwargs:
                selectmode = kwargs["selectmode"]

            # drinksContainer = Frame(self.myParent)
            container = Frame(tkParent)
            container.pack(side="left")

            # Label for the ingredient list
            Label(container, text=labelText).pack(side=TOP)

            # Frame for listbox and scrollbar
            frame = Frame(container)
            frame.pack()

            # Create the listbox
            self.listBox = Listbox(frame, selectmode=selectmode, height=30, exportselection=0)
            self.listBox.pack(side="right")

            # Create the scrollbar
            scrollBar = Scrollbar(frame, orient="vertical")
            scrollBar.config(command=self.listBox.yview())
            scrollBar.pack(side="left", fill="y")
            self.listBox.config(yscrollcommand=scrollBar.set) #Attach scrollbar to listbox

            if "selectFunction" in kwargs:
            #     # self.drinksListBox.bind('<<ListboxSelect>>',self.listBoxCurDrinkSelect)
                self.listBox.bind('<<ListboxSelect>>',kwargs["selectFunction"])

    def Ingredients(self, parent):
        kwargs = {"tkParent": parent,
                  "labelText": "Ingredients\nSelect multiple",
                  "selectmode": MULTIPLE,
                  "selectFunction": self.IngredientsCurSelect}
        self.ingredients =self.ScrollableListBox(**kwargs)

        # Import the data
        recipeLists = recipes()
        self.ingredientList =  recipeLists.listIngredients()
        self.recipeList = recipeLists.getRecipes()

        # Add the items to the list box
        for item in self.ingredientList:
            # print(item)
            self.ingredients.listBox.insert(END, item)

        ### How to remember state????
        try:
            with open("selectedIngredients.txt", "r", encoding="utf8") as file:
                for line in file:
                    idx = self.ingredientList.index(line.rstrip())
                    print(idx)
                    self.ingredients.listBox.selection_set(idx)
        except:
            # pass
            logging.debug("Couldn't find selectedIngredients.txt")
            traceback.print_exc()


    def Drinks(self, parent):
        kwargs = {"tkParent": parent,
                  "labelText": "Possible drinks\nSelect one",
                  "selectmode": SINGLE,
                  "selectFunction": self.DrinksCurSelect}
        self.drinks = self.ScrollableListBox(**kwargs)

    def Drinks1Missing(self, parent):
        kwargs = {"tkParent": parent,
                  "labelText": "Drinks missing 1 ingredient\nSelect one",
                  "selectmode": SINGLE,
                  "selectFunction": self.DrinksCurSelect}
        self.drinks1Missing = self.ScrollableListBox(**kwargs)

    class DisplayDrink:
        def __init__(self, tkParent):
            displayContainer = Frame(tkParent)
            displayContainer.pack(side="left")

            # Drink name:
            Label(displayContainer, text="Your selected drink:").pack(side=TOP)

            # Frame for listbox and scrollbar
            self.displayFrame = Frame(displayContainer)
            self.displayFrame.pack()

            # Put a picture in here
            self.OpenPicture()
            self.WriteRecipe()

        def OpenPicture(self, **kwargs):
            #Drink picture:
            maxWidth = 500
            maxHeight = 300
            try:
                imgPath = kwargs["drinkPicture"]
                img = Image.open(imgPath)
            except Exception:
                img = Image.open("images/dummy.png")
            finally: #Show the picture
                #Maintain the scaling
                # origScale = img.size[1]/img.size[2] # width / height -> width should be origScale * height
                widthSizeFactor = img.size[0] / maxWidth
                self.width = math.floor(img.size[0]/widthSizeFactor)
                self.height = math.floor(img.size[1]/widthSizeFactor)

                if self.height > maxHeight:
                    heightSizeFactor = img.size[1] / maxHeight
                    self.width = math.floor(img.size[0]/heightSizeFactor)
                    self.height = math.floor(img.size[1]/heightSizeFactor)

                img = img.resize((self.width,self.height), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)

                if "configure" in kwargs:
                    self.drinkImage.configure(image=img)
                else:
                    self.drinkImage = Label(self.displayFrame, image=img)
                    self.drinkImage.pack(side="top")

                self.drinkImage.image = img  # keep a reference! (So it doesn't get killed by the garbage collection)

        def WriteRecipe(self, **kwargs):
            widthScaling = 1.5

            if "configure" in kwargs:
                self.drinkName.configure(text=kwargs["drinkName"])
                self.drinkInstructions.configure(text=kwargs["instructions"])

                try:
                    self.drinkIngredients.destroy()
                except Exception:
                    pass
                finally:
                    bullet = "• "
                    ingredientText = ""
                    first = True
                    for i, (k, v) in enumerate(kwargs["ingredients"].items()):
                        if i == len(kwargs["ingredients"])-1: # Last bullet poitn
                            ingredientText = ingredientText + bullet + k + " " + v
                        elif first: # First bullet point
                            first = False
                            ingredientText = bullet + k + " " + v + "\n"
                        else: # Append to the string
                            ingredientText = ingredientText + bullet + k + " " + v + "\n"


                    self.drinkIngredients = Label(self.displayFrame, text=ingredientText, justify=LEFT, wraplength=math.floor(self.width/widthScaling), pady=2, font='Helvetica 10')
                    self.drinkIngredients.pack(side="top")

            else:
                self.drinkName = Label(self.displayFrame, text="Dummy drink name", wraplength=math.floor(self.width/widthScaling), pady=5, font='Helvetica 12 bold')
                self.drinkName.pack(side="top")

                self.drinkInstructions = Label(self.displayFrame, text="dummy instructions", justify=LEFT, wraplength=math.floor(self.width/widthScaling), pady=2, font='Helvetica 10')
                self.drinkInstructions.pack(side="top")

    def IngredientsCurSelect(self,event):
        selectedIngredients = []

        widget = event.widget
        selection = widget.curselection()
        for i in selection:
            selectedIngredients.append(widget.get(i))

        selectedIngredients = set(selectedIngredients)

        # call the PossibleDrinks function to update the possibleDrinks listbox
        self.PossibleDrinksUpdate(selectedIngredients)
        self.PossibleDrinks1MissingUpdate(selectedIngredients)

        with open("selectedIngredients.txt", "w", encoding="utf8") as file:
            for item in sorted(list(selectedIngredients)):
                file.write(item + "\n")

    def PossibleDrinksUpdate(self,selectedIngredients):
        possibleDrinks = []

        # Compare all the drinks in self.recipeList
        for k, v in self.recipeList.items():
            ingredientSet = set(v["ingredients"])
            if ingredientSet.issubset(selectedIngredients):
                possibleDrinks.append(k)

        self.drinks.listBox.delete(0,END)
        for item in possibleDrinks:
            self.drinks.listBox.insert(END, item)

    def PossibleDrinks1MissingUpdate(self,selectedIngredients):
        possibleDrinks1Missing = []

        # Compare all the drinks in self.recipeList
        for k, v in self.recipeList.items():
            ingredientSet = set(v["ingredients"])
            # print(ingredientSet)
            # print(selectedIngredients)
            if len(ingredientSet.difference(selectedIngredients)) == 1:
                possibleDrinks1Missing.append(k)

        self.drinks1Missing.listBox.delete(0,END)
        for item in possibleDrinks1Missing:
            self.drinks1Missing.listBox.insert(END, item)

    def DrinksCurSelect(self,event):
        widget = event.widget
        drinkSelection = widget.get(widget.curselection())
        drink = self.recipeList[drinkSelection]
        # print(drink)

        # Update the picture
        kwargs = {"drinkPicture":  drink["image"], "configure": True}
        self.displayDrink.OpenPicture(**kwargs)

        # Update the name
        kwargs = {"drinkName": drinkSelection, "instructions": drink["instructions"], "ingredients": drink["ingredients"], "configure": True}
        self.displayDrink.WriteRecipe(**kwargs)


class recipes():
    def __init__(self):
        # Load the data from the file
        try:
            with open("drinkRecipes.json", "r", encoding='utf-8') as jsonFile:
                self.recipeDict = json.load(jsonFile)
        except Exception:
            traceback.print_exc()
            print("*** You need to run the scrapeData.py script first to generate the json ***")

    def getRecipes(self):
        return self.recipeDict

    def listIngredients(self):
        listIngredient = []
        for k1, v1 in self.recipeDict.items():
            tmp = v1["ingredients"]
            for k2, v2 in tmp.items():
                listIngredient.append(str(k2))

        #Remove duplicates & sort alpabetically
        listIngredient = sorted(list(set(listIngredient)))
        return listIngredient

loggingConfig()
root = Tk()
drinksApp = DrinksApp(root)
root.mainloop()

