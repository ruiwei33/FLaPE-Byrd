#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 00:45:09 2021

@author: mtd
"""

from ReachObservations import ReachObservations
from ReachTruth import ReachTruth
from RiverIO import RiverIO
from FlowLawCalibration import FlowLawCalibration
from Domain import Domain
from FlowLaws import MWACN,MWAPN


# Read in data and initialize data objects
# IO=RiverIO('MetroManTxt',obsFname='PepsiSac/SWOTobs.txt',truthFname='PepsiSac/truth.txt')
BaseDir='/Users/mtd/OneDrive - The Ohio State University/Data/ArcticDEMHydro/reach_averages/gage22/'
IO=RiverIO('MetroManTxt',obsFname=BaseDir+'SWOTobs.txt',truthFname=BaseDir+'truth.txt')
D=Domain(IO.ObsData)
ConstrainHW_Switch=False
Obs=ReachObservations(D,IO.ObsData,ConstrainHW_Switch)
Truth=ReachTruth(IO.TruthData)

# check out heights and widths, and dA
Obs.plotHW()
Obs.plotdA()
Obs.plotHdA()

# Calibration calculations
Variants=['Constant-n', 'PowerLaw-n']

ReachData=[]
for r in range(0,D.nR):
    ReachDict={}
    ReachDict['dA']=Obs.dA[r,:]
    ReachDict['w']=Obs.w[r,:]
    ReachDict['S']=Obs.S[r,:]
    ReachDict['Qtrue']=Truth.Q[r,:]
    
    ReachData.append(ReachDict)

cals=[] #make a list of results, indexed by reach #
for r in range(0,D.nR):    
    FlowLawVariants={} #stash flow law variant objects for each reach in a dict       
    if 'Constant-n' in Variants:     
        FlowLawVariants['Constant-n']=MWACN(ReachData[r]['dA'],ReachData[r]['w'],ReachData[r]['S'])        
        
    if 'PowerLaw-n' in Variants:
        FlowLawVariants['PowerLaw-n']=MWAPN(ReachData[r]['dA'],ReachData[r]['w'],ReachData[r]['S'])           
           
    cal={} #make a dictionary of results, keyed off the flow law variant name
    for variant in FlowLawVariants.keys():               
        flow_law_cal=FlowLawCalibration(D,ReachData[r]['Qtrue'],FlowLawVariants[variant])
        flow_law_cal.CalibrateReach()
        cal[variant]=flow_law_cal

    cals.append(cal)

# Output
cals[0]['Constant-n'].PlotTimeseries()
cals[0]['Constant-n'].PlotScatterplot()
cals[0]['Constant-n'].Performance.ShowKeyErrorMetrics()
