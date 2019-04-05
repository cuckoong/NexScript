# converted from NexScript 'C:\Users\309i7\Documents\NeuroExplorer 5\Scripts\Shifting\ExtractEvents.nsc'
from __future__ import division
import nex
import math
import sys
import json

#combine all left/right stimulus (within same set of block), according to their side

doc = nex.GetActiveDocument()
filename = nex.GetDocTitle(doc)
print('You are extracting steady trials from this file: '+filename)

            
varnames = doc.EventNames()

#compare pro and anti block, see if they can match
Num_Pro_block =  sum(varname.startswith('Pro_steady_block') for varname in varnames)
Num_Anti_block =  sum(varname.startswith('Anti_steady_block') for varname in varnames)

print(Num_Pro_block,Num_Anti_block)




if Num_Pro_block != Num_Anti_block:
    print('Pro and Anti block are not paired')

else:

    for i in range(Num_Pro_block):
        #get the left/right stimulus in anti-block-i
        doc['Anti_steady_block_'+str(i)+'_Trial_Left'] = nex.IntFind(doc['Anti_steady_block_'+str(i)+'_Trial'], doc["LeftStimulus"])
        doc['Anti_steady_block_'+str(i)+'_Trial_Right'] = nex.IntFind(doc['Anti_steady_block_'+str(i)+'_Trial'], doc["RightStimulus"])
        
        #get the left/right stimulus in pro-block-i
        doc['Pro_steady_block_'+str(i)+'_Trial_Left'] = nex.IntFind(doc['Pro_steady_block_'+str(i)+'_Trial'], doc["LeftStimulus"])
        doc['Pro_steady_block_'+str(i)+'_Trial_Right'] = nex.IntFind(doc['Pro_steady_block_'+str(i)+'_Trial'], doc["RightStimulus"])
        
        #merge left//right stimulus in the same block
        doc['block_'+str(i)+'_Left'] = nex.IntOr(doc, doc['Anti_steady_block_'+str(i)+'_Trial_Left'], doc['Pro_steady_block_'+str(i)+'_Trial_Left'])
        doc['block_'+str(i)+'_Right'] = nex.IntOr(doc, doc['Anti_steady_block_'+str(i)+'_Trial_Right'], doc['Pro_steady_block_'+str(i)+'_Trial_Right'])