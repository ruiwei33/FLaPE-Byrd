#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:12:54 2021

@author: mtd
"""

from numpy import mean,sqrt,log,std

class ErrorStats:
    
    def __init__(self,Qt,Qhat,D):
    
        self.Qt=Qt
        self.Qhat=Qhat
        self.D=D
    
        self.RMSE=[];

    def CalcErrorStats(self):
        
        QhatAvg=mean(self.Qhat,axis=0)
        
        self.RMSE=sqrt(mean( (self.Qt-self.Qhat)**2 ) )
        
        self.rRMSE=sqrt(mean( ((self.Qt-self.Qhat)/self.Qt)**2  ) )        
        self.nRMSE=self.RMSE/mean(self.Qt)
          
        r=self.Qhat-self.Qt
        logr=log(self.Qhat)-log(self.Qt)
        
        self.NSE=1.-sum(r**2)/sum(  (self.Qt-QhatAvg)**2  )        
        
        self.VE=1.-sum(abs(r))/sum(self.Qt)
        
        self.bias=mean(r)
                        
        self.stdresid=std(r)        
        
        self.nbias = self.bias/QhatAvg
    
        self.MSC=log(  sum((self.Qt-QhatAvg)**2)/sum(r**2) -2*2 / self.D.nt  )
        self.meanLogRes=mean(logr)
        self.stdLogRes=std(logr)
        self.meanRelRes=mean(r/self.Qt)
        self.stdRelRes=std(r/self.Qt)
    
        self.Qbart=mean(self.Qt)  
    
    def ShowKeyErrorMetrics(self):
        print('Normalized RMSE:', '%.2f'%self.nRMSE)
        print('Normalized NSE:', '%.2f'%self.NSE)        