import json
import traceback
from tkinter import *


class DrinksApp:
    def __init__(self, parent):
        self.myParent = parent  ### (7) remember my parent, the root
        self.Ingredients()
        self.Drinks()

    def Ingredients(self):
        ingredientListContainer = Frame(self.myParent)
        ingredientListContainer.pack(side="left")

        # Label for the ingredient list
        Label(ingredientListContainer, text="Possible ingredients\nSelect multiple").pack(side=TOP)

        # Frame for listbox and scrollbar
        ingredientListFrame = Frame(ingredientListContainer)
        ingredientListFrame.pack()

        # Import the data
        recipeLists = recipes()
        self.ingredientList =  recipeLists.listIngredients()
        self.recipeList = recipeLists.getRecipes()

        # Create the listbox
        ingredientListBox = Listbox(ingredientListFrame, selectmode=MULTIPLE, height=30, exportselection=0)
        ingredientListBox.pack(side="right")
        for item in self.ingredientList:
            print(item)
            ingredientListBox.insert(END, item)

        # Create the scrollbar
        ingredientListScrollBar = Scrollbar(ingredientListFrame, orient="vertical")
        ingredientListScrollBar.config(command=ingredientListBox.yview())
        ingredientListScrollBar.pack(side="left", fill="y")
        ingredientListBox.config(yscrollcommand=ingredientListScrollBar.set) #Attach scrollbar to listbox

        ingredientListBox.bind('<<ListboxSelect>>',self.ingredientlistBoxCurSelect)

    def Drinks(self):
        drinksContainer = Frame(self.myParent)
        drinksContainer.pack(side="left")

        # Label for the ingredient list
        Label(drinksContainer, text="Possible drinks\nSelect one").pack(side=TOP)

        # Frame for listbox and scrollbar
        drinksFrame = Frame(drinksContainer)
        drinksFrame.pack()

        # Create the listbox
        self.drinksListBox = Listbox(drinksFrame, selectmode=SINGLE, height=30, exportselection=0)
        self.drinksListBox.pack(side="right")

        # Create the scrollbar
        drinksScrollBar = Scrollbar(drinksFrame, orient="vertical")
        drinksScrollBar.config(command=self.drinksListBox.yview())
        drinksScrollBar.pack(side="left", fill="y")
        self.drinksListBox.config(yscrollcommand=drinksScrollBar.set) #Attach scrollbar to listbox

        self.drinksListBox.bind('<<ListboxSelect>>',self.listBoxCurDrinkSelect)

    def ingredientlistBoxCurSelect(self,event):
        selectedIngredients = []

        widget = event.widget
        selection = widget.curselection()
        for i in selection:
            selectedIngredients.append(widget.get(i))

        selectedIngredients = set(selectedIngredients)
        # print(selectedIngredients)

        # call the PossibleDrinks function to update the possibleDrinks listbox
        print(self.PossibleDrinksUpdate(selectedIngredients))

    def PossibleDrinksUpdate(self,selectedIngredients):
        possibleDrinks = []

        # Compare all the drinks in self.recipeList
        for k, v in self.recipeList.items():
            ingredientSet = set(v["ingredients"])
            if ingredientSet.issubset(selectedIngredients):
                possibleDrinks.append(k)
            else:
                pass

        self.drinksListBox.delete(0,END)
        for item in possibleDrinks:
            self.drinksListBox.insert(END, item)

        return possibleDrinks

    def listBoxCurDrinkSelect(self,event):
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

