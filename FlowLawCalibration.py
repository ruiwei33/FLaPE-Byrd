#!/usr/bin/env python3
"""
Created on Thu Jan 21 04:49:20 2021

# -*- coding: utf-8 -*-
@author: mtd
"""

from scipy import optimize
from numpy import zeros
from ErrorStats import ErrorStats

import matplotlib.pyplot as plt

class FlowLawCalibration:
    def __init__(self,D,Qtrue,FlowLaw):
        self.D=D
        self.Qtrue=Qtrue
        self.FlowLaw=FlowLaw
        
        self.param_est=[]
        self.success=[]
        self.Qhat=[]
        self.Performance={}

    def CalibrateReach(self):     
        
        # self.param_est=zeros( (self.D.nR,2) )
        self.success= zeros( 1, dtype=bool )
        self.Qhat=zeros( (1,len(self.Qtrue)) )    
                   
        init_params=self.FlowLaw.GetInitParams()
        param_bounds=self.FlowLaw.GetParamBounds()         

            
        res = optimize.minimize(fun=self.ObjectiveFunc,
                                x0=init_params,
                                args=(self.Qtrue),
                                bounds=param_bounds )
        
        self.param_est=res.x
        self.success=res.success
        self.Qhat=self.FlowLaw.CalcQ(res.x)      
        
        self.Performance=ErrorStats(self.Qtrue,self.Qhat,self.D)
        self.Performance.CalcErrorStats()

    
    def ObjectiveFunc(self,params,Q):      
        Qhat=self.FlowLaw.CalcQ(params)
        y=sum((Qhat-Q)**2)
        return y


    def PlotTimeseries(self):
        fig,ax = plt.subplots()
        ax.plot(self.D.t.T,self.Qtrue,label='true')
        ax.plot(self.D.t.T,self.Qhat,label='estimate')        
        plt.title('Discharge timeseries')
        plt.xlabel('Time,days')
        plt.ylabel('Discharge m^3/s')
        plt.legend()        
        plt.show()
    def PlotScatterplot(self):
        fig,ax = plt.subplots()
        ax.scatter(self.Qtrue,self.Qhat,marker='o')        
        y_lim = ax.get_ylim()
        x_lim = ax.get_xlim()
        onetoone=[0,0]
        onetoone[0]=min(y_lim[0],x_lim[0])
        onetoone[1]=max(y_lim[1],x_lim[1])
        ax.plot([onetoone[0],onetoone[1]],[onetoone[0],onetoone[1]])
        plt.title('Discharge scatterplot')
        plt.xlabel('True Discharge m^3/s')
        plt.ylabel('Estimated Discharge m^3/s')      
        plt.show()   

        