# converted from NexScript 'C:\Users\309i7\Documents\NeuroExplorer 5\Scripts\Shifting\ExtractEvents.nsc'
from __future__ import division
import nex
import math
import sys

doc = nex.GetActiveDocument()

#extract events
#please refer to the arduino file
doc["TrialEnd"] = nex.MarkerExtract(doc, "Strobed", "=242,EOF,END")
doc["TrialStart"] = nex.MarkerExtract(doc, "Strobed", "=2,EOF,END")

#cue
doc["Cue"] = nex.MarkerExtract(doc, "Strobed", "=6,OR,=12,EOF,END")

doc["Pro"] = nex.MarkerExtract(doc, "Strobed", "=6,EOF,END")
doc["Anti"] = nex.MarkerExtract(doc, "Strobed", "=12,EOF,END")


#stimulus 
doc["stim"] = nex.MarkerExtract(doc, "Strobed", "=84,OR,=68,OR,=124,OR,=70,EOF,END")


#correct or mistake
doc["correct"] = nex.MarkerExtract(doc, "Strobed", "=10,OR,=64,EOF,END")
doc["Incorrect"] = nex.MarkerExtract(doc, "Strobed", "=48,EOF,END")
doc["Omission"] = nex.MarkerExtract(doc, "Strobed", "=240,EOF,END")
doc["Early"] = nex.MarkerExtract(doc, "Strobed", "=112,EOF,END")



#response
doc["Choice"] = nex.MarkerExtract(doc, "Strobed", "=26,OR,=4,EOF,END")


#make trials
#The interval include (trial start -2s) to Trial end(Choice or omission or early termination)
doc["Trial"] = nex.MakeIntFromStart(doc["TrialStart"], doc["TrialEnd"],  - 1.48, 1.48)
doc["ProTrial"] = nex.IntFind(doc["Trial"], doc["Pro"])
doc["AntiTrial"] = nex.IntFind(doc["Trial"], doc["Anti"])

#anti/pro cue epoch
doc["AntiCueEpoch"] = nex.MakeIntervals(doc["Anti"], 0, 1)
doc["ProCueEpoch"] = nex.MakeIntervals(doc["Pro"], 0, 1)

#1s before pro/anti cue 
doc["AntiCueBeforeEpoch"] = nex.MakeIntervals(doc["Anti"],  - 1, 0)
doc["ProCueBeforeEpoch"] = nex.MakeIntervals(doc["Pro"],  - 1, 0)
doc["CueBeforeEpoch"] = nex.MakeIntervals(doc["Cue"],  - 1, 0)

#1s after pro/anti cue 
doc["AntiCueAfterEpoch"] = nex.MakeIntervals(doc["Anti"], 0, 1)
doc["ProCueAfterEpoch"] = nex.MakeIntervals(doc["Pro"], 0, 1)
doc["CueAfterEpoch"] = nex.MakeIntervals(doc["Cue"], 0, 1)

#seperate trials into correct/incorrect/early/omission
doc["CorrectTrial"] = nex.IntFind(doc["Trial"], doc["correct"])
doc["inCorrectTrial"] = nex.IntFind(doc["Trial"], doc["Incorrect"])
doc["EarlyTrial"] = nex.IntFind(doc["Trial"], doc["Early"])
doc["OmissionTrial"] = nex.IntFind(doc["Trial"], doc["Omission"])


#check correct algorithm
doc["AntiCorrectTrial"] = nex.IntFind(doc["AntiTrial"], doc["correct"])
doc["AntiInCorrectTrial"] = nex.IntFind(doc["AntiTrial"], doc["Incorrect"])
doc["ProInCorrectTrial"] = nex.IntFind(doc["ProTrial"], doc["Incorrect"])
doc["ProCorrectTrial"] = nex.IntFind(doc["ProTrial"], doc["correct"])


#first pro/anti trial after anti/pro trial
doc["1st_Pro_AfterAnti"] = nex.FirstNAfter(doc["Pro"], doc["Anti"], 1)
doc["1st_Anti_AfterPro"] = nex.FirstNAfter(doc["Anti"], doc["Pro"], 1)
