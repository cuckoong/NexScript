

import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex

from __future__ import division
import nex
import math
import sys


def ExtractEvent():
doc = nex.GetActiveDocument()
#extract events
#please refer to the arduino file
doc["TrialEnd"] = nex.MarkerExtract(doc, "Strobed", "=242,EOF,END")
doc["TrialStart"] = nex.MarkerExtract(doc, "Strobed", "=2,EOF,END")
doc["Cue"] = nex.MarkerExtract(doc, "Strobed", "=6,OR,=12,EOF,END")
doc["Incorrect"] = nex.MarkerExtract(doc, "Strobed", "=48,EOF,END")
doc["correct"] = nex.MarkerExtract(doc, "Strobed", "=10,OR,=64,EOF,END")
doc["stim"] = nex.MarkerExtract(doc, "Strobed", "=84,OR,=68,OR,=124,OR,=70,EOF,END")
doc["Choice"] = nex.MarkerExtract(doc, "Strobed", "=26,OR,=4,EOF,END")


#make trials
#The interval include (trial start -2s) to Trial end(Choice or omission or early termination)
doc["Trial"] = nex.MakeIntFromStart(doc["TrialStart"], doc["TrialEnd"],  - 2, 0)


#seperate trials into correct/incorrect/early/omission

doc["CorrectTrial"] = nex.IntFind(doc["Trial"], doc["correct"])
doc["inCorrectTrial"] = nex.IntFind(doc["Trial"], doc["Incorrect"])
#doc["EarlyTrial"] = IntFind(doc["Trial"], doc["Early"])
#doc["OmissionTrial"] = IntFind(doc["Trial"], doc["Omission"])

#check correct algorithm


def MergeFile(InputPl2path,OutputNexPath,InputUnitspath)

InputPl2path = "C:\\Users\\309i7\\Documents\\NeuroExplorer 5\\Data\\TestDataFile5.nex"
OutputNexPath = "E:\\Panda\\TestFile.Nex5"
InputUnitspath = "E:\Panda\a.mat"

doc = nex.OpenDocument(InputPl2path)
print "Now processing the," + GetDocTitle(GetActiveDocument()) + "files"

#run ExtractEvents.nsc to extract events and make intervals
ExtractEvent()
#open matlab engine
nex.ExecuteMenuCommand("Matlab|Get Data From Matlab|Open Matlab As Engine")
#load the file contain units
loadFileStr = 'load("' + InputUnitspath + '");'
nex.ExecuteMatlabCommand(loadFileStr)
#GetVarFromMatlab(doc,"Units",1)
nex.SaveDocumentAs(doc, OutputNexPath)
nex.CloseDocument(doc)
