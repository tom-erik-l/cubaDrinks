import json
import traceback
from tkinter import *
from PIL import Image # pillow module
from PIL import ImageTk # pillow module
import math


class DrinksApp:
    def __init__(self, parent):
        self.myParent = parent  ### (7) remember my parent, the root
        self.Ingredients(parent)
        self.Drinks(parent)
        self.Drinks1Missing(parent)
        self.DisplayDrink()

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
                  "labelText": "Possible drinks\nSelect one",
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

    def DisplayDrink(self):
        displayContainer = Frame(self.myParent)
        displayContainer.pack(side="left")

        # Label for the ingredient list
        Label(displayContainer, text="Your selected drink:").pack(side=TOP)

        # Frame for listbox and scrollbar
        displayFrame = Frame(displayContainer)
        displayFrame.pack()

        # Drink name:
        Label(displayFrame, textvariable="Your selected drink:").pack(side=TOP)

        #Drink picture:
        maxWidth = 500
        maxHeight = 500
        try:
            img = Image.open("images/dummy.png")
        except Exception:
            img = Image.open("images/dummy.png")
        finally: #Show the picture
            #Maintain the scaling
            # origScale = img.size[1]/img.size[2] # width / height -> width should be origScale * height
            widthSizeFactor = img.size[0] / maxWidth
            width = math.floor(img.size[0]/widthSizeFactor)
            height = math.floor(img.size[1]/widthSizeFactor)

            if height > maxHeight:
                heightSizeFactor = img.size[1] / maxHeight
                width = math.floor(widthSizeFactor*img.size[0])
                height = math.floor(widthSizeFactor*img.size[1])

            img = img.resize((width,height), Image.ANTIALIAS)
            img =  ImageTk.PhotoImage(img)

            drinkImage = Label(displayFrame, image=img)
            drinkImage.image = img  # keep a reference! (So it doesn't get killed by the garbage collection)
            drinkImage.pack(side=TOP)

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
        pass
        # selectedIngredients = []

        # widget = event.widget
        # selection = widget.curselection()
        # for i in selection:
        #     selectedIngredients.append(widget.get(i))

        # selectedIngredients = set(selectedIngredients)
        # # print(selectedIngredients)




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


root = Tk()
drinksApp = DrinksApp(root)
root.mainloop()

