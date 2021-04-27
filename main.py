#options:
#   New Note
#   View/Edit Notes
#       Sort Notes
#   Delete Note
#   Note Statistics
#   Quit

from note import readNotes,printNotes,sortNotes,findNote
import json
import subprocess
import string
import re
from time import time_ns

from datetime import datetime
subprocess.run(["cls"], shell=True)


def getMainMenuOpt():
    options = ["new", "view", "edit", "delete", "stats", "quit"]
    print("  1) New Note")
    print("  2) View Notes")
    print("  3) Edit a Note")
    print("  4) Delete Note")
    print("  5) Note Statistics")
    print("  6) Quit")
    print()
    choice = int(input("Select an Option: "))
    return options[choice-1]

def getViewMenuOpt():
    sortOptions = ["date", "title"]
    filterOptions = ["category", "date", "title", "body"]

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
        if byDate == "n" or byDate == "N" or byDate == "No" or byDate == "no" or byDate == "":
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
            categories = input("Categories: ")
            body = input("Write your note: ")

            print ("\n")

            time = time_ns() #  = nanoseconds



            newNote["title"] = title
            newNote["categories"] = []
            if categories != "":
                newNote["categories"] = [category.strip() for category in categories.split(",")] #.split(",") converts to list
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

        if opt == "edit":
            subprocess.run("cls", shell=True)
            printNotes(notesList)
            print("-"*25, "\n"*3)
            print("* * Select a Note to Edit* *", "\n")
            userSelectionId = input("Input Note ID: ")

            foundNote = findNote(userSelectionId, notesList)
            print("\n"*2, "...note found...", "\n")
            print("-"*25)

            #revise selected note title with desired update
            print("Title: ", "\n", "    ", foundNote["title"], "\n")
            titleEdit = input("New Title? (input here): ")
            if titleEdit != "":
                foundNote["title"] = titleEdit

            #revise selected note categories with desired update
            print("\n")
            print("Categories: ", "\n", "    ", foundNote["categories"], "\n")
            categoriesEdit = input("New Categories? (input here): ").split(",")
            if categoriesEdit != "":
                foundNote["categories"] = categoriesEdit

            #revise selected note body with desired update
            print("\n")
            print("body: ", "\n", "    ", foundNote["body"], "\n")
            bodyEdit = input("New Body? (input here) ")
            if bodyEdit != "":
                foundNote["body"] = bodyEdit

            #updates selected note date to current time if edits occur
            if titleEdit != "" or categoriesEdit != "" or bodyEdit != "":
                foundNote["date"] = time_ns() #in nanoseconds

        if opt == "delete":
            subprocess.run("cls", shell=True)
            printNotes(notesList)
            print("-"*25, "\n"*3)
            print("* * Select a Note to Delete * *", "\n")
            userSelectionId = input("Input Note ID: ")

            foundNote = findNote(userSelectionId, notesList)
            print("\n"*2, "...note found...", "\n")


            printNotes([foundNote])

            confirm = input("Confirm note deletion? (y/n): ")
            if confirm == "Y" or confirm == "y" or confirm =="yes" or confirm == "Yes":
                notesList.remove(foundNote) #removes selected note from notesList
            else:
                print("\n", "Confirmation Failed", "\n")
        if opt == "stats":
            subprocess.run("cls", shell=True)
            print("-"*25,)
            print("Welcome to note statistics!")

            options=["num", "commonWord"]
            print(" 1) Number of notes")
            print(" 2) Most common word")
            print("\n")
            choice = options[int(input("Select an Option: "))-1]

            if choice == "num":
                print("Fetching data...", "\n"*2)
                print("You have written ", len(notesList), " notes!")

            if choice == "commonWord":
                wordCount={}

                for note in notesList:
                    bodyNoPunct = re.sub("[^\w\s]", "", note["body"]) # removes punctuation from each note["body"]
                    for word in bodyNoPunct.split(): # .split() is necessary to seperate words rather than letters
                        if word not in wordCount:
                            wordCount[word]=0 # creates word in dictionary if not already there
                        wordCount[word]+=1
                mostCommon = max(wordCount, key=wordCount.get) # max() finds key in dictionary with highest value

                print("\n","Your most frequent word, used ", wordCount[mostCommon], " times, was the word:", mostCommon, "\n")

        if opt == "quit":
            print ("Saving...")
            print("\n")
            print("Goodbye...")
            break

    file.seek(0)
    file.truncate()
    json.dump(notesList, file)




main()
