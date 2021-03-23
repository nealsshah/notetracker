#options:
#   New Note
#   View/Edit Notes
#       Sort Notes
#   Delete Note
#   Note Statistics
#   Quit

from note import readNotes,printNotes,sortNotes
import json
import subprocess
from time import time_ns

from datetime import datetime
subprocess.run(["cls"], shell=True)


def getMainMenuOpt():
    options = ["new", "view", "delete", "stats", "quit"]
    print("  1) New Note")
    print("  2) View/Edit Notes")
    print("  3) Delete Note")
    print("  4) Note Statistics")
    print("  5) Quit")
    print()
    choice = int(input("Select an Option: "))
    return options[choice-1]

def getViewMenuOpt():
    sortOptions = ["date", "title"]
    filterOptions = ["category", "date", "title", "body"]
    # BUG with following: if sortQuerry or filterQuerry ==  variation of "no" -> error
        # SOLUTION: move if byDate - if byTitle within if sortQuerry | move if filtCategory - if filtBody within
        # if filterQuerry
            # new BUG: current options {} placement resets user choices
                # SOLUTION: move options {} to beginning of function
                    # see myEdits.py file
    byDate = "no"
    byTitle = "no"
    order = "asc"

    filtCategory = ""
    filtDate = ""
    filtTitle = ""
    filtBody = ""

    sortQuerry = input("Would you like to sort? ")
    if sortQuerry == "y" or sortQuerry == "Y" or sortQuerry == "yes" or sortQuerry == "Yes":
        byDate = input("  By Date? ")
        if byDate == "n" or byDate == "N" or byDate == "No" or byDate == "no":
            byTitle = input("  By Title? ")
        order = input("  Direction? (asc/desc) ")
    fitlerQuerry = input("Would you like to filter? ")
    if fitlerQuerry == "y" or fitlerQuerry == "Y" or fitlerQuerry == "yes" or fitlerQuerry == "Yes":
        filtCategory = input("  Enter Category(s)? ")
        filtDate = input("  Enter date / date range? [mm/dd/yyyy (- mm/dd/yyyy)] ")
        filtTitle = input("  Enter title keyword(s)? ")
        filtBody = input("  Enter body keyword(s)? ")

    options = {
    "sorting":{
        "date": True,
        "title": False,
        "order": "asc"
    },
    "filters":{
        "categories": [],
        "date": {
        "start": datetime.min,
        "end": datetime.today(),
        },
        "title": [],
        "body": []
    }
    }

    if byDate == "n" or byDate == "N" or byDate == "No" or byDate == "no":
        options["sorting"]["date"] = False
    if byTitle == "y" or byTitle == "Y" or byTitle == "Yes" or byTitle == "yes":
        options["sorting"]["title"] = True
    if order != "":
        options["sorting"]["order"] = order
    if filtCategory != "":
        options["filters"]["categories"] = [category.strip() for category in filtCategory.split(",")]
    if filtDate != "":
        dates = [date.strip() for date in filtDate.split("-")]
        dateStart = datetime.strptime(dates[0],"%m/%d/%Y")
        options["filters"]["date"]["start"] = dateStart
        if len(dates) < 2:
            options["filters"]["date"]["end"] = dateStart
        else:
            options["fitlers"]["date"]["end"] = datetime.strptime(dates[1],"%m/%d/%Y")

    if filtTitle != "":
        options["filters"]["title"] = [title.strip() for title in filtTitle.split(",")]
    if filtBody != "":
        options["filters"]["body"] = [keyword.strip() for keyword in filtBody.split(",")]


    return options


def intersect(aList, bList):
    return [a for a in aList if a in bList]





def main():
    # opens file containing all notes
    notesList = []
    try:
        file = open("noteDB.json", 'r+')
        notesList = readNotes(file)
    except IOError:
        file = open("noteDB.json", 'w+')


    while True:
        print("-"*25)
        print("Welcome to Note Tracker")
        opt = getMainMenuOpt()
        if opt == "new":
            subprocess.run(["cls"], shell=True)
            print ("* * New Note * *")
            print ("\n")

            newNote = {}

            title = input("Title: ")
            categories = input("Categories: ").split(",")
            body = input("Write your note: ")

            print ("\n")

            time = time_ns() #  = nanoseconds



            newNote["title"] = title
            newNote["categories"] = [category.strip() for category in categories]
            newNote["body"] = body
            newNote["date"] = time
            newNote["id"] = time


            notesList.append(newNote)
        if opt == "view":
            subprocess.run("cls", shell=True)
            print ("* * View Notes * *", "\n")

            options = getViewMenuOpt()

            subprocess.run("cls", shell=True)
            print("* * Results * *")


            filterList = notesList
            if len(options["filters"]["categories"]) != 0:
                filterList = [note for note in notesList for cat in options["filters"]["categories"] if cat in note["categories"]]
            filterListB = filterList
            if len(options["filters"]["title"]) != 0:
                filterListB = [note for note in filterList for titleKey in options["filters"]["title"] if titleKey in note["title"]]
            filterListC = filterListB
            if len(options["filters"]["body"]) != 0:
                filterListC = [note for note in filterListB for bodyKey in options["filters"]["body"] if bodyKey in note["body"]]

            if options["sorting"]["date"]:
                sortedNotes = sortNotes(filterListC,"date", options["sorting"]["order"])
            else:
                sortedNotes = sortNotes(filterListC,"title", options["sorting"]["order"])


            printNotes(sortedNotes)

            

        if opt == "delete":
            print ("Delete a note")
        if opt == "stats":
            print("Access Note Statistics")
        if opt == "quit":
            print ("Saving...")
            print("\n")
            print("Goodbye...")
            break

    file.seek(0)
    file.truncate()
    json.dump(notesList, file)




main()
