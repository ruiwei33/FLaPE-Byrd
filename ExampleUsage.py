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

IO=RiverIO('MetroManTxt',obsFname='ArcticDEMSag/SWOTobs.txt',truthFname='ArcticDEMSag/truth.txt')
D=Domain(IO.ObsData)

obs=ReachObservations(D,IO.ObsData)
truth=ReachTruth(IO.TruthData)
cal=FlowLawCalibration(D,obs,truth)
