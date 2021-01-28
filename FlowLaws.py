#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 04:50:53 2021

@author: mtd
"""

from numpy import inf

class FlowLaws:
    
    def __init__(self,dA,W,S):
        self.dA=dA
        self.W=W
        self.S=S       #plan is to switch these to Obs                
        
        self.params=[]
        self.init_params=[]        
        
        
class FlowLawVariant1(FlowLaws):
    def __init__(self,dA,W,S):
        super().__init__(dA,W,S)        
        

    def CalcQ(self,params):
        Q=1/params[0]*(params[1]+self.dA)**(5/3)*self.W**(-2/3)*self.S**(1/2)
        return Q
    def GetInitParams(self):
        #etc
        init_params=[.03, 500]
        return init_params
    def GetParamBounds(self):
        #etc
        param_bounds=( (.001, 1)  , (-min(self.dA)+1,inf) )
        return param_bounds

# class FlowLawVariant2(FlowLaws):
#         def CalcQ(self,params):
#             n=self.params[0]*((self.params[1]+self.dA)/self.W)**self.params[2]
#             Q=n*(self.params[1]+self.dA)**(5/3)*self.W**(-2/3)*self.S**(1/2)
#             return Q
#         def GetInitParams(self):
#             #etc
#             init_params=[.03, 500]
#             return init_params       