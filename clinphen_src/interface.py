import sys
import os
import re
import webbrowser

myDir = "/".join(os.path.realpath(__file__).split("/")[:-1])
sys.path.append(myDir)

import umlshelp
import get_phenotypes
from appJar import gui
import tkFont as font
from Tkinter import *

from get_phenotypes import *


default_thesaurus = myDir + "/data/hpo_synonyms.txt"
umls_thesaurus = myDir + "/data/hpo_umls_thesaurus.txt"
hpo_main_names = myDir + "/data/hpo_term_names.txt"
syns = load_all_hpo_synonyms()
results = ""



bigDiv = 30
medDiv = 45
smallDiv = 75
bigLabels = ["Title"]
medLabels = ["pickThesaurusLabel", "giveRecordLabel", "extractLabel", "ResultsLabel", "saveLabel"]
smallLabels = ["Description", "haveUMLS", "CustomThesaurusInstructions", "hpoDescription", 
                #"umlsDescription"
                "customDescription", "recordFileDescription", "recordTextDescription", "copyDescription", "saveDescription", "allLabel", "fourLabel", "excelDescription", "tabLabel", "commaLabel", "limitLabel", "formatLabel", "idListLabel"]
messages = []
buttons = ["Select custom thesaurus", "Get UMLS Metathesaurus", "Extract", "Copy", "Select medical record", "Save", "giveRecordHelp", "Excel"]
radioButtons = ["thesaurusChoice", "recordFormat", "phenoLimit", "saveFormat"]
entries = ["customThesaurusEntry", "recordFile"]
links = ["For more information, see the manuscript."]
grids = ["resultsTable"]
textAreas = ["Record"]
screenWidth = 0
screenHeight = 0
windowWidth = 0
i = 0

def run_gui():
    global screenWidth
    global screenHeight
    global windowWidth
    ClinPhen = gui()
    #ClinPhen.setGeometry("fullscreen")

    screenWidth = ClinPhen.topLevel.winfo_screenwidth()
    screenHeight = ClinPhen.topLevel.winfo_screenheight()
    ClinPhen.setGeometry(int(screenWidth / 1.25), int(screenHeight / 1.25))

    ClinPhen.setStretch("both")
    ClinPhen.setSticky("nesw")

    ClinPhen.setTitle("ClinPhen")
    ClinPhen.setBg("grey")
    ClinPhen.startScrollPane("MainScroll")
    
    def getNames():
      returnMap = {}
      for line in open(hpo_main_names):
        lineData = line.strip().split("\t")
        returnMap[lineData[0]] = lineData[1]
      return returnMap
    hpo_to_name = getNames()

    def extract(button):
      global results
      recForm = ClinPhen.getRadioButton("recordFormat")
      if recForm == "File":
        if not os.path.isfile(ClinPhen.getEntry("recordFile")):
          ClinPhen.infoBox("Error", "Please provide a valid file path to the medical record.")
          return
        recFile = ClinPhen.getEntry("recordFile")
        record = ""
        for line in open(recFile): record += line
      else: record = ClinPhen.getTextArea("Record")
      if ClinPhen.getRadioButton("thesaurusChoice") == "Custom":
        custom_thesaurus = ClinPhen.getEntry("customThesaurusEntry")
        if not os.path.isfile(custom_thesaurus):
          ClinPhen.infoBox("Error", "Please provide a valid file path to the custom thesaurus.")
          return
        thesaurus = custom_thesaurus
      elif ClinPhen.getRadioButton("thesaurusChoice") == "UMLS":
        if not os.path.isfile(umls_thesaurus):
          ClinPhen.infoBox("Error", "Please install the UMLS Metathesaurus before you choose the \"UMLS\" option.")
        thesaurus = umls_thesaurus
      else: thesaurus = default_thesaurus
      results = extract_phenotypes_custom_thesaurus(record, thesaurus, hpo_to_name)
      placeGrid(gridLoc)
      #ClinPhen.setMessage("Results", results)

    def copy(button):
      global results
      terminalResults = results
      if ClinPhen.getRadioButton("phenoLimit") == "Top 4": terminalResults = "\n".join(terminalResults.split("\n")[:5])
      terminalResults = re.sub("\n", "___", terminalResults)
      terminalResults = re.sub("\t", "__", terminalResults)
      if ClinPhen.getRadioButton("saveFormat") == "Comma-separated": command = "echo \"" + terminalResults + "\" | sed 's/___/\\'$'\\n/g' | sed 's/,//g' | sed 's/__/,/g' | pbcopy"
      elif ClinPhen.getRadioButton("saveFormat") == "HPO ID list":
        HPO_IDs = []
        for line in terminalResults.split("___"):
          HPO_ID = line.split("__")[0]
          if "HP:" in HPO_ID: HPO_IDs.append(HPO_ID)
        terminalResults = ",".join(HPO_IDs)
        command = "echo \"" + terminalResults + "\" | pbcopy"
      else: command = "echo \"" + terminalResults + "\" | sed 's/___/\\'$'\\n/g' | sed 's/__/\\'$'\\t/g' | pbcopy"
      os.system(command)
    
    def rescaleWidgets():
      ClinPhen.setLabelWidth("Title", 40)
      for label in bigLabels: ClinPhen.getLabelWidget(label).config(font="Times "+str(windowWidth/bigDiv)+" bold")
      for label in medLabels: ClinPhen.getLabelWidget(label).config(font="Times "+str(windowWidth/medDiv)+" bold")
      for label in smallLabels: ClinPhen.getLabelWidget(label).config(font="Times "+str(windowWidth/smallDiv))
      for message in messages: ClinPhen.getMessageWidget(message).config(font="Times "+str(windowWidth/smallDiv))
      for button in buttons: ClinPhen.getButtonWidget(button).config(font="Times "+str(windowWidth/smallDiv), fg="black")
      for entry in entries: ClinPhen.getEntryWidget(entry).config(font="Times "+str(windowWidth/smallDiv))
      for textArea in textAreas: ClinPhen.getTextAreaWidget(textArea).config(font="Times "+str(windowWidth/smallDiv))
      for rbutton in radioButtons:
        for rbn in ClinPhen.getRadioButtonWidget(rbutton): rbn.config(font="Times "+str(windowWidth/smallDiv)+" bold", fg="black")
      for link in links: ClinPhen.getLinkWidget(link).config(font="Times "+str(windowWidth/smallDiv))
      for grid in grids:
        ClinPhen.confGrid(grid, "font", font.Font(family="Times", size=windowWidth/smallDiv))

    def checkSize(event="None"):
      global windowWidth
      newWidth = ClinPhen.topLevel.winfo_width()
      newHeight = ClinPhen.topLevel.winfo_height()
      if windowWidth == newWidth:
        return
      windowWidth = newWidth
      rescaleWidgets()

    def customThesaurus(button):
      custom_thesaurus = ClinPhen.openBox(title="Custom thesaurus")
      ClinPhen.setEntry("customThesaurusEntry", custom_thesaurus)

    def thesaurusChoice(button):
      choice = ClinPhen.getRadioButton("thesaurusChoice")
      if choice == "HPO": pass
      else: pass
      if choice == "Custom":
        ClinPhen.showEntry("customThesaurusEntry")
        ClinPhen.showButton("Select custom thesaurus")
      else:
        ClinPhen.hideEntry("customThesaurusEntry")
        ClinPhen.hideButton("Select custom thesaurus")
      if choice == "UMLS":
        updateHaveUMLS()
        ClinPhen.showLabel("haveUMLS")
        ClinPhen.showButton("Get UMLS Metathesaurus")
      else:
        ClinPhen.hideLabel("haveUMLS")
        ClinPhen.hideButton("Get UMLS Metathesaurus")

    def updateHaveUMLS():
      if os.path.isfile(umls_thesaurus):
        ClinPhen.setLabel("haveUMLS", "You have a processed UMLS Metathesaurus.\nGo ahead and run the extractor!")
      else:
        ClinPhen.setLabel("haveUMLS", "You do not have a processed UMLS Metathesaurus.\nInstall it before you use this option.")


    def startUMLSHelp(button):
      umlshelp.run_gui()
      #os.system("python " + myDir + "/umlshelp.py")
      updateHaveUMLS()

    def recordFormat(button):
      if ClinPhen.getRadioButton("recordFormat") == "Text":
        ClinPhen.showTextArea("Record")
        ClinPhen.hideEntry("recordFile")
        ClinPhen.hideButton("Select medical record")
      else:
        ClinPhen.hideTextArea("Record")
        ClinPhen.showEntry("recordFile")
        ClinPhen.showButton("Select medical record")

    def selectMedicalRecord(button):
      record = ClinPhen.openBox(title="Select medical record")
      ClinPhen.setEntry("recordFile", record)

    def saveResults(button):
      saveLoc = ClinPhen.saveBox(title="Save", asFile=True)
      global results
      saveResults = results
      if ClinPhen.getRadioButton("phenoLimit") == "Top 4": saveResults = "\n".join(saveResults.split("\n")[:5])
      if ClinPhen.getRadioButton("saveFormat") == "Comma-separated": saveResults = re.sub("\t", ",", re.sub(",", "", saveResults))
      elif ClinPhen.getRadioButton("saveFormat") == "HPO ID list":
        HPO_IDs = []
        for line in saveResults.split("\n"):
          HPO_ID = line.split("\t")[0]
          if "HP:" in HPO_ID: HPO_IDs.append(HPO_ID)
        saveResults = ",".join(HPO_IDs)
      #print saveLoc
      #writeFile = open(saveLoc, "w+")
      #writeFile.write(saveResults)
      #writeFile.close()
      saveLoc.write(saveResults)
      saveLoc.close()

    def placeGrid(gridLoc):
      global results
      data = []
      #data.append(["HPO ID", "Phenotype name", "No. occurrences", "Earliness (lower = earlier)", "Example sentence"])
      for line in results.split("\n"): data.append(line.strip().split("\t"))
      ClinPhen.openScrollPane("MainScroll")
      #ClinPhen.setGridData("resultsTable", data)
      ClinPhen.removeGrid("resultsTable")
      ClinPhen.addGrid("resultsTable", data, gridLoc, 0, 3, action=viewHPO)
      ClinPhen.getGridWidget("resultsTable").config(actionheading="View in HPO", actionbutton="View")
      ClinPhen.stopScrollPane()
      rescaleWidgets()

    def excel(button):
      saveLoc = myDir + "/misc/Untitled.txt"
      global results
      saveResults = results
      if ClinPhen.getRadioButton("phenoLimit") == "Top 4": saveResults = "\n".join(saveResults.split("\n")[:5])
      writeFile = open(saveLoc, "w+")
      writeFile.write(saveResults)
      writeFile.close()
      os.system("open " + saveLoc + " -a \"Microsoft Excel\"")
      #os.system("rm " + saveLoc)

    def viewHPO(button):
      global results
      hpoid = results.split("\n")[int(button) + 1].split("\t")[0]
      webbrowser.open("http://compbio.charite.de/hpoweb/showterm?id=" + hpoid)

    def ipp():
      global i
      returnInt = i
      i += 1
      return returnInt

    ClinPhen.addLabel("Title", "Welcome to ClinPhen!", ipp(), 0, 3)
    ClinPhen.addButton("Credits", (lambda button: ClinPhen.infoBox("Credits", "Copyright 2018 Cole A. Deisseroth, Johannes Birgmeier, Ethan E. Bodle, Jennefer Kohler, Dena Matalon, Yelena Nazarenko, Casie A. Genetti, Catherine A. Brownstein, Klaus Schmitz-Abe, Kelly Schoch, Heidi Cope, Rebecca Signer, Undiagnosed Diseases Network, Julian A. Martinez-Agosto, Vandana Shashi, Alan H. Beggs, Matthew T. Wheeler, Jonathan A. Bernstein, Gill Bejerano.\nSoftware uses appJar, provided by Richard Jarvis.\nSpecial thanks to Elijah Kravets and the Bejerano Lab for helping us improve the software.")), i-1, 0)
    ClinPhen.addLabel("Description", "ClinPhen is a tool that extracts Human Phenotype Ontology (HPO) phenotypes from a medical record.\nPhenotypes are listed in order of:\n\t1. Number of times mentioned (descending)\n\t2. Earliest mention\n\t3. HPO ID (ascending)", ipp(), 0, 3)
    ClinPhen.addWebLink("For more information, see the manuscript.", "https://www.ncbi.nlm.nih.gov/pubmed/30514889", ipp(), 0, 3)

    ClinPhen.addHorizontalSeparator(ipp(), 0, 3)

    ClinPhen.addLabel("pickThesaurusLabel", "Step 1: Select a thesaurus", ipp(), 1)
    ClinPhen.addLabel("CustomThesaurusInstructions", "A thesaurus is a database containing phrases that match each HPO phenotype.\nClinPhen checks for each HPO phenotype by looking for the phrases that correspond to it.", ipp(), 1)
    ClinPhen.addRadioButton("thesaurusChoice", "Default", i, 0)
    ClinPhen.addLabel("hpoDescription", "The default HPO thesaurus provided with the HPO database", ipp(), 1)
    ClinPhen.setLabelAlign("hpoDescription", "left")
    #ClinPhen.addRadioButton("thesaurusChoice", "UMLS", i, 0)
    #ClinPhen.addLabel("umlsDescription", "An expanded HPO thesaurus provided by the Unified Medical Language System (UMLS)", ipp(), 1)
    #ClinPhen.setLabelAlign("umlsDescription", "left")
    ClinPhen.addRadioButton("thesaurusChoice", "Custom", i, 0)
    ClinPhen.addLabel("customDescription", "Provide your own custom HPO thesaurus, with the following format for each row: HPO_ID<tab>Matching_Phrase", ipp(), 1)
    ClinPhen.setLabelAlign("customDescription", "left")
    ClinPhen.setRadioButtonChangeFunction("thesaurusChoice", thesaurusChoice)
    ClinPhen.addEntry("customThesaurusEntry", i, 1)
    ClinPhen.addButton("Select custom thesaurus", customThesaurus, i, 2)
    ClinPhen.addLabel("haveUMLS", "We have not checked if you have UMLS...", ipp(), 1)
    ClinPhen.addButton("Get UMLS Metathesaurus", startUMLSHelp, ipp(), 1)

    ClinPhen.addHorizontalSeparator(ipp(), 0, 3)

    ClinPhen.addButton("giveRecordHelp", (lambda button: ClinPhen.infoBox("How to get a patient's clinical notes as a plain-text file", "1. Log onto EPIC hyperspace\n2. Open the medical record of the patient of interest\n3. Click on \"Chart Review\"\n4. Go to the \"Notes/Trans\" tab\n5. Use Ctrl-Click to select all of the clinical notes you are interested in. The best notes for genetic disease diagnosis are usually the \"Progress Notes\" (column: \"Note Type\") from the \"Genetics\" department (column: \"Specialty (Dept.)\").\n6. Once all notes of interest are selected, click \"Review Selected\"\n7. Right-click the text body and select \"Copy All\".\n8. Paste the text directly into the box in the ClinPhen window, or into a plain-text file (.txt, for instance) which you can then upload.")), i, 0)
    ClinPhen.setButton("giveRecordHelp", "Help")
    ClinPhen.addLabel("giveRecordLabel", "Step 2: Insert a medical record", ipp(), 1)
    ClinPhen.addRadioButton("recordFormat", "File", i, 0)
    ClinPhen.addLabel("recordFileDescription", "Load the patient's medical record, as a plain-text file.", ipp(), 1)
    ClinPhen.setLabelAlign("recordFileDescription", "left")
    ClinPhen.addRadioButton("recordFormat", "Text", i, 0)
    ClinPhen.addLabel("recordTextDescription", "Paste in the patient's free-text medical record.", ipp(), 1)
    ClinPhen.setLabelAlign("recordTextDescription", "left")
    ClinPhen.addEntry("recordFile", i, 1)
    ClinPhen.addButton("Select medical record", selectMedicalRecord, i, 2)
    ClinPhen.addScrolledTextArea("Record", ipp(), 1)
    ClinPhen.setRadioButtonChangeFunction("recordFormat", recordFormat)

    ClinPhen.addHorizontalSeparator(ipp(), 0, 3)

    ClinPhen.addLabel("extractLabel", "Step 3: Run the extractor", ipp(), 1)
    ClinPhen.addButton("Extract", extract, ipp(), 1)


    ClinPhen.addHorizontalSeparator(ipp(), 0, 3)

    ClinPhen.addLabel("ResultsLabel", "Extracted phenotypes are displayed below.", ipp(), 1)
    gridLoc = i
    ClinPhen.addGrid("resultsTable", [["HPO ID", "Phenotype name", "No. occurrences", "Earliness (lower = earlier)", "Example sentence"]], ipp(), 0, 3, action=viewHPO)
    ClinPhen.getGridWidget("resultsTable").config(actionheading="View in HPO", actionbutton="View")

    ClinPhen.addHorizontalSeparator(ipp(), 0, 3)

    ClinPhen.addLabel("saveLabel", "Step 4: Save the results", ipp(), 1)

    ClinPhen.addLabel("limitLabel", "Phenotype limit", ipp(), 0)
    ClinPhen.addRadioButton("phenoLimit", "All", i, 0)
    ClinPhen.addLabel("allLabel", "Copy/save all of the phenotypes listed. Recommended for most purposes.", ipp(), 1, 3)
    ClinPhen.setLabelAlign("allLabel", "left")
    ClinPhen.addRadioButton("phenoLimit", "Top 4", i, 0)
    ClinPhen.addLabel("fourLabel", "Copy/save the first 4 phenotypes listed. Recommended if you are using an automatic gene-ranking tool for Mendelian disease diagnosis.", ipp(), 1, 3)
    ClinPhen.setLabelAlign("fourLabel", "left")

    ClinPhen.addLabel("formatLabel", "Output format", ipp(), 0)
    ClinPhen.addRadioButton("saveFormat", "Tab-separated", i, 0)
    ClinPhen.addLabel("tabLabel", "Copy/save a tab-separated table", ipp(), 1, 3)
    ClinPhen.setLabelAlign("tabLabel", "left")
    ClinPhen.addRadioButton("saveFormat", "Comma-separated", i, 0)
    ClinPhen.addLabel("commaLabel", "Copy/save a comma-separated table", ipp(), 1, 3)
    ClinPhen.setLabelAlign("commaLabel", "left")
    ClinPhen.addRadioButton("saveFormat", "HPO ID list", i, 0)
    ClinPhen.addLabel("idListLabel", "Copy/save a comma-separated list of the HPO IDs", ipp(), 1, 3)
    ClinPhen.setLabelAlign("idListLabel", "left")

    ClinPhen.addLabel("copyDescription", "Copy the results to the clipboard. Results can be pasted into Excel.", i, 1)
    ClinPhen.setLabelAlign("copyDescription", "left")
    ClinPhen.addButton("Copy", copy, ipp(), 0)
    ClinPhen.addLabel("saveDescription", "Save the results as a tab-delimited table.", i, 1)
    ClinPhen.setLabelAlign("saveDescription", "left")
    ClinPhen.addButton("Save", saveResults, ipp(), 0)
    ClinPhen.addLabel("excelDescription", "Open the results in Excel.", i, 1)
    ClinPhen.setLabelAlign("excelDescription", "left")
    ClinPhen.addButton("Excel", excel, ipp(), 0)

    ClinPhen.stopScrollPane()
    rescaleWidgets()
    thesaurusChoice("")
    recordFormat("")
    updateHaveUMLS()
    ClinPhen.topLevel.bind("<Configure>", checkSize)
    ClinPhen.go()

if __name__ == "__main__": run_gui()
