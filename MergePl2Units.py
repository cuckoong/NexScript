import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex



InputPl2path = "C:\\Users\\309i7\\Documents\\NeuroExplorer 5\\Data\\TestDataFile5.nex"
OutputNexPath = "E:\\Panda\\TestFile.Nex5"
#InputUnitspath = ".mat"

doc = nex.OpenDocument(InputPl2path)
#Msg("Now processing the, GetDocTitle(GetActiveDocument()), files")

#run ExtractEvents.nsc to extract events and make intervals
nex.RunScript("C:\\Users\\309i7\\Documents\\NeuroExplorer 5\\Scripts\\Shifting\\ExtractEvents.nsc")
#open matlab engine
nex.ExecuteMenuCommand("Matlab|Get Data From Matlab|Open Matlab As Engine")

#load the file contain units
nex.ExecuteMatlabCommand("load(E:\Panda\PandaData\ShiftingData\20181220)")
#GetVarFromMatlab(doc,"Units",1)
nex.SaveDocumentAs(doc, OutputNexPath)
nex.CloseDocument(doc)
