#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 23:49:40 2021

@author: mtd
"""

from numpy import reshape,concatenate,zeros,ones,triu,empty

class ReachObservations:    
        
    def __init__(self,D,RiverData):
        
        self.D=D
        
        # assign data from input dictionary
        self.h=RiverData["h"]           
        self.w=RiverData["w"]
        self.S=RiverData["S"]
        self.h0=RiverData["h0"]
        self.sigh=RiverData["sigh"]
        self.sigw=RiverData["sigw"]
        self.sigS=RiverData["sigS"]
        
        # et al.
        self.GetVectorObs()            
        
        self.CalcdA()
    
    def GetVectorObs(self):    
        
        #%% create resahepd versions of observations
        self.hv=reshape(self.h, (self.D.nR*self.D.nt,1) )
        self.Sv=reshape(self.S, (self.D.nR*self.D.nt,1) )
        self.wv=reshape(self.w, (self.D.nR*self.D.nt,1) )

  

            
    def CalcdA(self):
    
        DeltaAHat=empty( (self.D.nR,self.D.nt-1) )
        
        for r in range(0,self.D.nR):
            for t in range(0,self.D.nt-1):
                DeltaAHat[r,t]=(self.w[r,t]+self.w[r,t+1])/2 * (self.h[r,t+1]-self.h[r,t])
         
        # changed how this part works compared with Matlab, avoiding translating calcU
        DeltaAHatv=reshape(DeltaAHat,(self.D.nR*(self.D.nt-1),1) )
        
        self.dA= concatenate(  (zeros( (self.D.nR,1) ), DeltaAHat @ triu(ones( (self.D.nt-1,self.D.nt-1) ),0)),1 ) 
                
        U=self.D.CalcU()
        self.dAv=U @ DeltaAHatv
    
        # Note that the below commented command is equivalent, but "U" is needed in
        #   other functions, and this is a good test for consistency
        #Obs.dAv=reshape(Obs.dA, (D.nR*D.nt,1)) 
        

        