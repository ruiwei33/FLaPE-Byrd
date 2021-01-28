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
from pprint import pprint
from FlowLaws import *

IO=RiverIO('MetroManTxt',obsFname='PepsiSac/SWOTobs.txt',truthFname='PepsiSac/truth.txt')

# BaseDir='/Users/mtd/Box/Data/ArcticDEMHydro/reach_averages/sag_32/'
# IO=RiverIO('MetroManTxt',obsFname=BaseDir+'SWOTobs.txt',truthFname=BaseDir+'truth.txt')
D=Domain(IO.ObsData)

Obs=ReachObservations(D,IO.ObsData)
Truth=ReachTruth(IO.TruthData)

Variants=[1, 2]

cals={}

for r in range(0,D.nR):
    dA=Obs.dA[r,:]
    W=Obs.w[r,:]
    S=Obs.S[r,:]
    Qtrue=Truth.Q[r,:]
    
    FlowLawVariants=[]       
    if 1 in Variants:     
        FlowLawVariants.append(FlowLawVariant1(dA,W,S) )
    if 2 in Variants:
        FlowLawVariants.append(FlowLawVariant2(dA,W,S) )
       
    cal={}
    for i in range(0,len(FlowLawVariants) ):
        cal[i]=FlowLawCalibration(D,dA,W,S,Qtrue,FlowLawVariants[i])       
        cal[i].CalibrateReaches()
    
    cals[r]=cal

pprint(vars(cals[1][0].Performance))

pprint(vars(cals[1][1].Performance))

