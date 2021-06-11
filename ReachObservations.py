#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 23:49:40 2021
@author: mtd
"""

from numpy import reshape,concatenate,zeros,ones,triu,empty,arctan,tan,pi
from scipy import stats
import matplotlib.pyplot as plt
import copy

class ReachObservations:    
        
    def __init__(self,D,RiverData,ConstrainHWSwitch=False):
        
        self.D=D    
        self.ConstrainHWSwitch=ConstrainHWSwitch
        
        
        # assign data from input dictionary
        self.h=RiverData["h"]           
        self.w=RiverData["w"]
        self.S=RiverData["S"]
        self.h0=RiverData["h0"]
        self.sigh=RiverData["sigh"]
        self.sigw=RiverData["sigw"]
        self.sigS=RiverData["sigS"]    
        
        # optionally constrain heights and widths to be self-consistent
        if ConstrainHWSwitch:
            self.ConstrainHW()

        #%% create resahepd versions of observations
        self.hv=reshape(self.h, (self.D.nR*self.D.nt,1) )
        self.Sv=reshape(self.S, (self.D.nR*self.D.nt,1) )
        self.wv=reshape(self.w, (self.D.nR*self.D.nt,1) )
        
        DeltaAHat=empty( (self.D.nR,self.D.nt-1) )
        self.DeltaAHatv = self.calcDeltaAHatv(DeltaAHat)
        self.dA= concatenate(  (zeros( (self.D.nR,1) ), DeltaAHat @ triu(ones( (self.D.nt-1,self.D.nt-1) ),0)),1 )
        self.dAv=self.D.CalcU() @ self.DeltaAHatv

    def calcDeltaAHatv(self, DeltaAHat):
        
        for r in range(0,self.D.nR):
            for t in range(0,self.D.nt-1):
                DeltaAHat[r,t]=(self.w[r,t]+self.w[r,t+1])/2 * (self.h[r,t+1]-self.h[r,t])
         
        # changed how this part works compared with Matlab, avoiding translating calcU
        return reshape(DeltaAHat,(self.D.nR*(self.D.nt-1),1) )
    
    def ConstrainHW(self):
        
        # save a copy of 
        self.hobs=copy.deepcopy(self.h[0,:])
        self.wobs=copy.deepcopy(self.w[0,:])
        
        self.fit = stats.linregress(self.hobs, self.wobs)        

        mo=-tan(pi/2-arctan(self.fit.slope));
        self.h[0,:]=(self.wobs-mo*self.hobs-self.fit.intercept)/(self.fit.slope-mo);
        self.w[0,:]=self.fit.slope*self.h+self.fit.intercept;                
        
    def plotHW(self):
        fig,ax = plt.subplots()
        
        if self.ConstrainHWSwitch:
            ax.scatter(self.hobs,self.wobs,marker='o')   
            ax.scatter(self.h[0,:],self.w[0,:],marker='o')   
        else: 
            ax.scatter(self.h[0,:],self.w[0,:],marker='o')   
            
        plt.title('WSE vs width for first reach')
        plt.xlabel('WSE, m')
        plt.ylabel('Width, m')      
        plt.show() 
        
    def plotdA(self):
        fig,ax = plt.subplots()
        ax.plot(self.D.t.T,self.dA[0,:])        
            
        plt.title('dA timeseries')
        plt.xlabel('Time, days')
        plt.ylabel('dA, m^2')      
        plt.show()       
        
    def plotHdA(self):
        fig,ax = plt.subplots()
        
        ax.scatter(self.h[0,:],self.dA[0,:],marker='o')   
            
        plt.title('dA vs WSE for first reach')
        plt.xlabel('WSE, m')
        plt.ylabel('dA, m')      
        plt.show()         
