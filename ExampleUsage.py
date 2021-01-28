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

# IO=RiverIO('MetroManTxt',obsFname='PepsiSac/SWOTobs.txt',truthFname='PepsiSac/truth.txt')

BaseDir='/Users/mtd/Box/Data/ArcticDEMHydro/reach_averages/sag_32/'
IO=RiverIO('MetroManTxt',obsFname=BaseDir+'SWOTobs.txt',truthFname=BaseDir+'truth.txt')
D=Domain(IO.ObsData)

# Variant={"1"}

obs=ReachObservations(D,IO.ObsData)
truth=ReachTruth(IO.TruthData)
cal=FlowLawCalibration(D,obs,truth)
cal.CalibrateReaches()

pprint(vars(cal.Performance[0]))