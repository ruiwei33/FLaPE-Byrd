#!/usr/bin/env python3
"""
Created on Thu Jan 21 04:49:20 2021

# -*- coding: utf-8 -*-
@author: mtd
"""

from scipy import optimize
from numpy import inf,zeros,mean,sqrt,log,std
from ErrorStats import ErrorStats
from FlowLaws import *

class FlowLawCalibration:
    def __init__(self,D,Obs,Truth):
        self.D=D
        self.Obs=Obs
        self.Truth=Truth
        self.Performance={}
        self.FlowLaw=[]  

    def CalibrateReaches(self):     
        
        self.param_est=zeros( (self.D.nR,2) )
        self.success= zeros( (self.D.nR,1), dtype=bool )
        self.Qhat=zeros( (self.D.nR,self.D.nt) )                
        
        for r in range(0,self.D.nR):
        
            dA=self.Obs.dA[r,:]
            W=self.Obs.w[r,:]
            S=self.Obs.S[r,:]
            Q=self.Truth.Q[r,:]
            
            self.FlowLaw=FlowLawVariant1(dA,W,S) #next need to enable calling func to specify list of flow law variants to iterate over
            
            init_params=self.FlowLaw.GetInitParams()
            param_bounds=self.FlowLaw.GetParamBounds()            
            
            res = optimize.minimize(fun=self.ObjectiveFunc,
                                    x0=init_params,
                                    args=(dA,W,S,Q),
                                    bounds=param_bounds )
            
            self.param_est[r,:]=res.x
            self.success[r]=res.success
            self.Qhat[r,:]=self.FlowLaw.CalcQ(res.x)      
            
            self.Performance[r]=ErrorStats(Q,self.Qhat[r,:],self.D)
            self.Performance[r].CalcErrorStats()

    
    def ObjectiveFunc(self,params,dA,W,S,Q):      
        Qhat=self.FlowLaw.CalcQ(params)
        y=sum((Qhat-Q)**2)
        return y


        