#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 04:50:53 2021

@author: mtd
"""

from numpy import inf, log10

class FlowLaws:
    
    def __init__(self,dA,W,S,h):
        self.dA=dA
        self.W=W
        self.S=S       #plan is to switch these to Obs                
        self.h=h
        self.params=[]
        self.init_params=[]                
        
class MWACN(FlowLaws):
    # this flow law is Manning's equation, wide-river approximation, area-formulation, 
    #   constant friction coefficient, no channel shape assumption: MWACN
    def __init__(self,dA,W,S,h):
        super().__init__(dA,W,S,h)        
        
    def CalcQ(self,params):
        Q=1/params[0]*(params[1]+self.dA)**(5/3)*self.W**(-2/3)*self.S**(1/2)
        return Q
    def GetInitParams(self):
        #etc
        init_params=[.03, 350]
        return init_params
        #etc
    def GetParamBounds(self):
        param_bounds=( (.001, 1), (-min(self.dA)+1,inf) )
        return param_bounds

class MWAPN(FlowLaws):
    # this flow law is Manning's equation, wide-river approximation, area-formulation, 
    #   powerlaw  friction coefficient, no channel shape assumption: MWAPN
    def __init__(self,dA,W,S,h):
        super().__init__(dA,W,S,h)     
    def CalcQ(self,params):
        n=params[0]*((params[1]+self.dA)/self.W)**params[2]
        Q=1/n*(params[1]+self.dA)**(5/3)*self.W**(-2/3)*self.S**(1/2)
        return Q
    def GetInitParams(self):
        #etc
        init_params=[.03, 350,1]
        return init_params       
    def GetParamBounds(self):
        #etc
        param_bounds=( (.001, 1), (-min(self.dA)+1,inf), (-inf,inf) )
        return param_bounds       
    
class HiVDI(FlowLaws):
    def __init__(self,dA,W,S,h):
        super().__init__(dA,W,S,h)     
    def CalcQ(self,params):
        np=params[0]*((params[1]+self.dA)/self.W)**params[2]
        Q=np*(params[1]+self.dA)**(5/3)*self.W**(-2/3)*self.S**(1/2)
        return Q
    def GetInitParams(self):
        #etc
        init_params=[1/.03, 350, -1]
        return init_params       
    def GetParamBounds(self):
        #etc
        param_bounds=( (1, 1/.001), (-min(self.dA)+1,inf), (-inf,inf) )
        return param_bounds   

        return param_bounds 
    
class MOMMA(FlowLaws):
    def __init__(self,dA,W,S,h):
        super().__init__(dA,W,S,h)     
    def CalcQ(self,params):
        nb=0.11*(params[2])**0.18
        n=nb*(1+log10( (params[1] - params[0])/(self.h - params[0]) ))
        Q=1/n*((self.h - params[0])*(2/3))**(5/3)*self.W*self.S**(1/2)
        return Q
    def GetInitParams(self):
        #etc
        init_params=[2, 13, 0.0001]
        return init_params       
    def GetParamBounds(self):
        #etc
        param_bounds=((0, 50), (10, 60), (0, inf) )
        return param_bounds 