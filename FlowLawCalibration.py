#!/usr/bin/env python3
"""
Created on Thu Jan 21 04:49:20 2021

# -*- coding: utf-8 -*-
@author: mtd
"""

from scipy import optimize
from numpy import inf,zeros,mean,sqrt,log,std
from ErrorStats import ErrorStats
# from FlowLaws import *

class FlowLawCalibration:
    def __init__(self,D,dA,W,S,Qtrue,FlowLaw):
        self.D=D
        self.dA=dA
        self.W=W
        self.S=S
        self.Qtrue=Qtrue
        self.FlowLaw=FlowLaw
        self.Performance={}

    def CalibrateReaches(self):     
        
        # self.param_est=zeros( (self.D.nR,2) )
        self.success= zeros( 1, dtype=bool )
        self.Qhat=zeros( (1,self.D.nt) )    
                   
        init_params=self.FlowLaw.GetInitParams()
        param_bounds=self.FlowLaw.GetParamBounds()         

            
        res = optimize.minimize(fun=self.ObjectiveFunc,
                                x0=init_params,
                                args=(self.dA,self.W,self.S,self.Qtrue),
                                bounds=param_bounds )
        
        self.param_est=res.x
        self.success=res.success
        self.Qhat=self.FlowLaw.CalcQ(res.x)      
        
        self.Performance=ErrorStats(self.Qtrue,self.Qhat,self.D)
        self.Performance.CalcErrorStats()

    
    def ObjectiveFunc(self,params,dA,W,S,Q):      
        Qhat=self.FlowLaw.CalcQ(params)
        y=sum((Qhat-Q)**2)
        return y


        