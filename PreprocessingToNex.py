import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex
from glob import glob


def extractevents():
    doc = nex.GetActiveDocument()
    # extract events
    # please refer to the arduino file
    doc["TrialEnd"] = nex.MarkerExtract(doc, "Strobed", "=242,EOF,END")
    doc["TrialStart"] = nex.MarkerExtract(doc, "Strobed", "=2,EOF,END")
    doc["Cue"] = nex.MarkerExtract(doc, "Strobed", "=6,OR,=12,EOF,END")
    doc["Incorrect"] = nex.MarkerExtract(doc, "Strobed", "=48,EOF,END")
    doc["correct"] = nex.MarkerExtract(doc, "Strobed", "=10,OR,=64,EOF,END")
    doc["stim"] = nex.MarkerExtract(doc, "Strobed", "=84,OR,=68,OR,=124,OR,=70,EOF,END")
    doc["Choice"] = nex.MarkerExtract(doc, "Strobed", "=26,OR,=4,EOF,END")

    # make trials
    # The interval include (trial start -2s) to Trial end(Choice or omission or early termination)
    doc["Trial"] = nex.MakeIntFromStart(doc["TrialStart"], doc["TrialEnd"], - 2, 0)

    # seperate trials into correct/incorrect/early/omission

    doc["CorrectTrial"] = nex.IntFind(doc["Trial"], doc["correct"])
    doc["inCorrectTrial"] = nex.IntFind(doc["Trial"], doc["Incorrect"])
    # doc["EarlyTrial"] = IntFind(doc["Trial"], doc["Early"])
    # doc["OmissionTrial"] = IntFind(doc["Trial"], doc["Omission"])

    # check correct algorithm

def mergefile(input):
    # run ExtractEvents.nsc to extract events and make intervals
    inputpl2path = ''.join(glob(input + "2DigitalRefPl2\\*.pl2"))
    outputnexpath = ''.join(glob(input + "7NexFiles\\Refpl2.nex5"))
    inputunitspath = ''.join(glob(input + "2DigitalRefPl2\\SingleUnitsForNex.mat"))
    inputunittextpath = ''.join(glob(input + '6SingleUnit\\NeuroList.txt'))
    doc = nex.OpenDocument(inputpl2path)
    #print "Now processing the,"
    #print  nex.GetDocTitle(nex.GetActiveDocument())
    extractevents()
    f = open(inputunittextpath,'r')
    allunits = f.read()
    allunits = allunits[:-2]
    units = allunits.split("/n")
    f.close()

    # open matlab engine
    nex.ExecuteMenuCommand("Matlab|Get Data From Matlab|Open Matlab As Engine")
    # load the file contain units
    loadfilestr = 'load("' + inputunitspath + '");'
    print loadfilestr
    nex.ExecuteMatlabCommand(loadfilestr)

    for name in units:
        nex.GetVarFromMatlab(doc,name,1)

    nex.SaveDocumentAs(doc, outputnexpath)
    nex.CloseDocument(doc)
    print 'Finish the file '+outputnexpath
