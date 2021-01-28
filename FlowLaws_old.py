#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 04:50:53 2021

@author: mtd
"""

# unfinished garble... saving in case useful later

class FlowLaws_old:
    
    def __init__(self,dA,W,S,Variant):
        self.dA=dA
        self.W=W
        self.S=S       

        self.Qfunc=[]
        
        self.Variant=Variant

        self.Q=[]
        self.params=[]
        
    
    def CalcQ(self):
        if self.Variant=="1":
            self.Q=1/self.params[0]*(self.params[1]+self.dA)**(5/3)*self.W**(-2/3)*self.S**(1/2)
        elif self.Variant=="2":
            n=self.params[0]*((self.params[1]+self.dA)/self.W)**self.params[2]
            self.Q=n*(self.params[1]+self.dA)**(5/3)*self.W**(-2/3)*self.S**(1/2)

            
 
            