#!/usr/bin/env python3
"""
Created on Thu Jan 21 04:49:20 2021

# -*- coding: utf-8 -*-
@author: mtd
"""

from scipy import optimize
from numpy import inf,zeros,mean,sqrt,log,std
from ErrorStats import ErrorStats

class FlowLawCalibration:
    def __init__(self,D,Obs,Truth):
        self.D=D
        self.Obs=Obs
        self.Truth=Truth
        self.Performance={}
        
        
    def ManningVariant1(self,params,dA,W,S):
        Q=1/params[0]*(params[1]+dA)**(5/3)*W**(-2/3)*S**(1/2)
        return Q
    
    def ManningVariant2(self,params,dA,W,S):
        n=params[0]*((params[1]+dA)/W)**params[2]
        Q=n*(params[1]+dA)**(5/3)*W**(-2/3)*S**(1/2)
        return Q    

    def CalibrateReaches(self):     
        
        self.param_est=zeros( (self.D.nR,2) )
        self.success= zeros( (self.D.nR,1), dtype=bool )
        self.Qhat=zeros( (self.D.nR,self.D.nt) )
        
        for r in range(0,self.D.nR):
        
            dA=self.Obs.dA[r,:]
            W=self.Obs.w[r,:]
            S=self.Obs.S[r,:]
            Q=self.Truth.Q[r,:]
            
            init_params=[.03, 500]
            
            param_bounds=( (.001, 1)  , (-min(dA)+1,inf) )
            
            res = optimize.minimize(fun=self.ObjectiveFunc,
                                    x0=init_params,
                                    args=(dA,W,S,Q),
                                    bounds=param_bounds )
            
            self.param_est[r,:]=res.x
            self.success[r]=res.success
            self.Qhat[r,:]=self.ManningVariant1(self.param_est[r,:],dA,W,S)
            
            # self.CalcErrorStats(Q, self.Qhat[r]) #super sloppy        
            self.Performance[r]=ErrorStats(Q,self.Qhat[r,:])
            self.Performance[r].CalcErrorStats()

    
    def ObjectiveFunc(self,params,dA,W,S,Q):      
        # Qhat=1/params[0]*(params[1]+dA)**(5/3)*W**(-2/3)*S**(1/2)
        Qhat=self.ManningVariant1(params,dA,W,S)
        y=sum((Qhat-Q)**2)
        return y


        