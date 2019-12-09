import sys
import os
import re

#TODO: Mention the phenotype name and description
#TODO: Resize the items in the GUI
#TODO: allow pasting in of files
from appJar import gui
#from clinphen_src.get_phenotypes import *

bigDiv = 30
medDiv = 50
smallDiv = 70
bigLabels = ["Title"]
medLabels = ["Results"]
smallLabels = ["Description", "Instructions"]
webLinks = ["Licensed UMLS users can download the latest release of the Metathesaurus here"]
buttons = ["Extract", "Select UMLS folder"]
entries = ["umlsDir"]
myDir = "/".join(os.path.realpath(__file__).split("/")[:-1])
targetDir = myDir + "/data/"
prepperPath = myDir + "/prep_thesaurus.py"
getterPath = myDir + "/umls_thesaurus_extraction.sh"
screenWidth = 0
screenHeight = 0
windowWidth = 0
windowHeight = 0

def run_gui():
    UMLSHelp = gui()
    scaleFactor = 0.75
    global screenWidth
    global screenHeight
    global windowWidth
    global windowHeight
    screenWidth = UMLSHelp.topLevel.winfo_screenwidth()
    screenHeight = UMLSHelp.topLevel.winfo_screenheight()
    windowWidth = int(screenWidth * scaleFactor)
    windowHeight = int(screenHeight * scaleFactor)
    UMLSHelp.setGeometry(str(windowWidth) + "x" + str(windowHeight))
    def umlsExtract(button):
      umlsDir = UMLSHelp.getEntry("umlsDir")
      results = os.popen(" ".join(["bash -e", getterPath, umlsDir, targetDir, prepperPath, "2>&1 >/dev/null"])).readline()
      if not results:
        UMLSHelp.setLabel("Results", "Extraction successful :)")
      else: UMLSHelp.setLabel("Results", results)

    def rescaleWidgets():
        UMLSHelp.setLabelWidth("Title", 50)
        for label in bigLabels: UMLSHelp.getLabelWidget(label).config(font="Times "+str(windowWidth/bigDiv)+" bold")
        for label in medLabels: UMLSHelp.getLabelWidget(label).config(font="Times "+str(windowWidth/medDiv)+" bold")
        for label in smallLabels: UMLSHelp.getLabelWidget(label).config(font="Times "+str(windowWidth/smallDiv))
        for button in buttons: UMLSHelp.getButtonWidget(button).config(font="Times "+str(windowWidth/smallDiv))
        for entry in entries: UMLSHelp.getEntryWidget(entry).config(font="Times "+str(windowWidth/smallDiv))
        for webLink in webLinks: UMLSHelp.getLinkWidget(webLink).config(font="Times "+str(windowWidth/smallDiv))


    def checkSize(event="None"):
        global windowWidth
            #global windowHeight
        newWidth = UMLSHelp.topLevel.winfo_width()
        newHeight = UMLSHelp.topLevel.winfo_height()
        if windowWidth == newWidth:
            return
        windowWidth = newWidth
        #windowHeight = newHeight
        rescaleWidgets()

    def pickUMLSDir(button):
      dir = UMLSHelp.directoryBox(title="Select unzipped UMLS folder")
      UMLSHelp.setEntry("umlsDir", dir)

    UMLSHelp.setTitle("UMLS metathesaurus extraction")
    UMLSHelp.setBg("grey")
    UMLSHelp.startScrollPane("MainScroll")
    UMLSHelp.addLabel("Title", "Getting UMLS", 0, 0)
    UMLSHelp.addLabel("Description", "While not necessary, the UMLS Metathesaurus can considerably improve the performance of UMLSHelp.\nWe can't just give out the Metathesaurus to everyone though--that would be illegal.", 1, 0)
    UMLSHelp.addWebLink("Licensed UMLS users can download the latest release of the Metathesaurus here", "https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html", 2, 0)
    UMLSHelp.addLabel("Instructions", "Once you have downloaded and unzipped the UMLS data folder, select the folder below, and it will be processed into a thesaurus for UMLSHelp.", 3, 0)
    UMLSHelp.addEntry("umlsDir", 4, 0)
    UMLSHelp.addButton("Select UMLS folder", pickUMLSDir, 4, 1)
    UMLSHelp.addButton("Extract", umlsExtract, 5, 0)
    UMLSHelp.addLabel("Results", "", 6, 0)

    UMLSHelp.stopScrollPane()
    UMLSHelp.topLevel.bind("<Configure>", checkSize)
    checkSize()
    UMLSHelp.go()

if __name__ == "__main__": run_gui()
