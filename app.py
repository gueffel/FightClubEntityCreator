import tkinter as tk
from tkinter import filedialog, Text, ttk
import os
import json

root = tk.Tk()
root.title("Bravo Setup")
root.geometry("500x250")
root.configure(background="#333640", padx=10, pady=10)
root.iconbitmap("C:/Users/gueffel/Desktop/FightClubEntityCreator/img/ODS.ico")

bravoFilePath = ""
filePathSize = len(bravoFilePath)
bravoFilePathShortened = ""

scenariosPath = ""
scenarios = []

selectedScenario = tk.StringVar()
selectedScenario.set("Select your scenario file")
currentScenario = ""

selectedEntity = tk.StringVar()
selectedEntity.set("Select your assigned entity")

def selectBravoPath():
    global bravoFilePath
    global bravoFilePathShortened
    global scenariosPath
    global scenarios
    global scenarioDropDown

    filename = filedialog.askopenfilename(initialdir="/", title="Select your Bravo.exe file",
    filetypes=(("Bravo Executable", "Bravo.exe"), ("All Files", "*.*")))
    bravoFilePath=filename
    bravoFilePathShortened=filename[:filePathSize - 10]
    selectBravoExeButton.config(text="bravo.exe selected!")

    scenariosPath=bravoFilePathShortened + "/bravo/Scenarios/"
    scenarios=os.listdir(scenariosPath)
    scenarioDropDown = tk.OptionMenu(root, selectedScenario, *scenarios, command=scenarioSelected)
    scenarioDropDown.pack()

    return bravoFilePath, bravoFilePathShortened, scenariosPath, scenarios, scenarioDropDown

def scenarioSelected(*args):
    global currentScenario
    currentScenario = selectedScenario.get()
    selectedScenarioPath = scenariosPath + currentScenario
    scenarioDataFile = open(selectedScenarioPath)
    scenarioData = json.load(scenarioDataFile)

    entities = []

    for entity in scenarioData["entities"]:
        entities.append(entity["id"])

    entityDropDown = tk.OptionMenu(root, selectedEntity, *entities, command=entitySelected)
    entityDropDown.pack()

def entitySelected(*args):
    writeJSONFileButton.pack()

def writeBravoJSON():
    filePathNameWExt = bravoFilePathShortened + "/bravo/" + "client.json"
    data = {}
    data["server"] = "97.107.177.9"
    data["admin"] = "false"
    data["entity"] = selectedEntity.get()
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

    startBravoText.pack()
    startBravoButton.pack()

def startBravo():
    os.startfile(bravoFilePath)
    root.destroy()

introText = tk.Label(root, text="This application will guide you through the quick setup \nprocess for Bravo. Do this before you start Bravo for the first time.\n", fg="white", bg="#333640")
introText.pack()

selectBravoExeButton = tk.Button(root, text="Find your bravo.exe from the zip file you downloaded", padx=10, pady=5, fg="white", bg="#42a4c8", command=selectBravoPath)
selectBravoExeButton.pack()

writeJSONFileButton = tk.Button(root, text="Finish Setup", padx=10, pady=5, fg="white", bg="#42a4c8", command=writeBravoJSON)

startBravoText = tk.Label(root, text = "Done, now let's start Bravo!", fg="white", bg="#333640")

startBravoButton = tk.Button(root, text="Start Bravo and close this app", padx=10, pady=5, fg="white", bg="#42a4c8", command=startBravo)

root.mainloop()