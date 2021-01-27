#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:12:54 2021

@author: mtd
"""

from numpy import mean,sqrt

class ErrorStats:
    
    def __init__(self,Qt,Qhat):
    
        self.Qt=Qt
        self.Qhat=Qhat
    
        self.RMSE=[];

    def CalcErrorStats(self):
        
        QhatAvg=mean(self.Qhat,axis=0)
        
        self.RMSE=sqrt(mean( (self.Qt-QhatAvg)**2 ) )
        
        # self.ErrorStats={}    
        
        # self.ErrorStats["RMSE"]=sqrt(mean( (Qt-QhatAvg)**2 ) )
        # self.ErrorStats["rRMSE"]=sqrt(mean( (  (Qt-QhatAvg)/Qt   )**2 ) )
        # self.ErrorStats["nRMSE"]=self.ErrorStats["RMSE"]/mean(Qt)
          
        # r=QhatAvg-Qt
        # logr=log(QhatAvg)-log(Qt)
    
        # self.ErrorStats["NSE"]=1-sum(r**2)/sum( (Qt-mean(Qt))**2 )
        # self.ErrorStats["VE"]=1- sum(abs(r))/sum(Qt)
    
        # self.ErrorStats["bias"]=mean(r)
        # self.ErrorStats["stdresid"]=std(r)
        # self.ErrorStats["nbias"] = self.ErrorStats["bias"]/mean(Qt)
    
        # self.ErrorStats["MSC"]=log(  sum((Qt-mean(Qt))**2)/sum(r**2) -2*2 / self.D.nt  )
        # self.ErrorStats["meanLogRes"]=mean(logr)
        # self.ErrorStats["stdLogRes"]=std(logr)
        # self.ErrorStats["meanRelRes"]=mean(r/Qt)
        # self.ErrorStats["stdRelRes"]=std(r/Qt)
    
        # self.ErrorStats["Qbart"]=mean(Qt)  