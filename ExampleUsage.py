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
BaseDir='/Users/mtd/Box/Data/ArcticDEMHydro/reach_averages/sag_32/'
IO=RiverIO('MetroManTxt',obsFname=BaseDir+'SWOTobs.txt',truthFname=BaseDir+'truth.txt')
D=Domain(IO.ObsData)
Obs=ReachObservations(D,IO.ObsData)
Truth=ReachTruth(IO.TruthData)

# Calibration calculations
Variants=['Constant-n', 'PowerLaw-n']
ReachData={} #stash reach data in a dictionary
for r in range(0,D.nR):
    dA=Obs.dA[r,:]
    W=Obs.w[r,:]
    S=Obs.S[r,:]
    Qtrue=Truth.Q[r,:]
    ReachData[r]=[dA,W,S,Qtrue]

cals={}
for r in range(0,D.nR):    
    FlowLawVariants={} #stash flow law variant objects for each reach in a dict       
    if 'Constant-n' in Variants:     
        FlowLawVariants['Constant-n']=MWACN(ReachData[r][0],ReachData[r][1],ReachData[r][2])
        
    if 'PowerLaw-n' in Variants:
        FlowLawVariants['PowerLaw-n']=MWAPN(ReachData[r][0],ReachData[r][1],ReachData[r][2])
       
    cal=[]
    for variant in FlowLawVariants.keys():               
        flow_law_cal=FlowLawCalibration(D,ReachData[r][3],FlowLawVariants[variant])
        flow_law_cal.CalibrateReach()
        cal.append(flow_law_cal)        
    
    cals[r]=cal

# Output
cals[0][0].PlotTimeseries()
cals[0][0].PlotScatterplot()
cals[0][0].Performance.ShowKeyErrorMetrics()
