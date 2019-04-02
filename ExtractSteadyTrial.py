# converted from NexScript 'C:\Users\309i7\Documents\NeuroExplorer 5\Scripts\Shifting\ExtractEvents.nsc'
from __future__ import division
import nex
import math
import sys
import json


doc = nex.GetActiveDocument()
filename = nex.GetDocTitle(doc)
print('You are extracting steady trials from this file: '+filename)

#usually the first channel is 1st_Anti_AfterPro
#The second channel is 1st_Pro_AfterAnti
first_Anti_AfterSwitch = nex.GetVarByName(doc,'1st_Anti_AfterPro').Timestamps()
first_Pro_AfterSwitch =  nex.GetVarByName(doc,'1st_Pro_AfterAnti').Timestamps()
ProTs =  nex.GetVarByName(doc,'Pro').Timestamps()
AntiTs = nex.GetVarByName(doc,'Anti').Timestamps()

Num_Pro_Steady = len(first_Anti_AfterSwitch)
Num_Anti_Steady = len(first_Pro_AfterSwitch)
print('Steady Trials in Pro Task has '+str(Num_Pro_Steady)+' blocks')
print('Steady Trials in Anti Task has '+str(Num_Anti_Steady)+' blocks')



#This is event based on pro and anti cue.
def GetSteadyBlock(Num_Steady,TrialTs,first_AfterSwitch,TrialType):
    #Get steady block from pro/anti trials
    for i in range(Num_Steady):
        steady_all_ts = [ts for ts in TrialTs if ts <= first_AfterSwitch[i]]
        steady_ts = steady_all_ts[-20:]
        #get the steady timestamp from last 20 trials
        print('1st '+TrialType+' trial after switch: '+ str(first_AfterSwitch[i]))
        print('the timestamps for the last 20 previous kind of trials before switch: '+str(steady_ts))  
        
        #add the timestamp as event in the file with name formated as pre/anti_steady_block_num_trial
        name_steady_block = TrialType + '_steady_block_'+str(i)
        doc[name_steady_block] = nex.NewEvent(doc, 0) 
        for j in steady_ts:
            temp = nex.GetVarByName(doc,name_steady_block)
            nex.AddTimestamp(temp,j)
            doc[name_steady_block+'_Trial'] = nex.MakeIntervals(doc[name_steady_block], 0, 1)

GetSteadyBlock(Num_Anti_Steady,AntiTs,first_Pro_AfterSwitch,'Anti')
GetSteadyBlock(Num_Pro_Steady,ProTs,first_Anti_AfterSwitch,'Pro')
