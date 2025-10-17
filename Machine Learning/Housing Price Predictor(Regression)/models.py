# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 11:01:09 2025

@author: Shivam Kumar yadav
"""

import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import(LinearRegression,Ridge,Lasso,SGDRegressor,ElasticNet,HuberRegressor)
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import lightgbm as lgb
import xgboost as xgb
from sklearn.metrics import (mean_absolute_error,mean_squared_error,r2_score)
import pickle


data=pd.read_csv(r"C:\Users\Shivam Kumar yadav\OneDrive\Desktop\FSDS\Machine Learning (ML)\Self_Practice\house project Regression\USA_Housing.csv")

#X=data.drop(['Price','Address'],axis=1)

X=data.iloc[:,:5]
y=data.iloc[:,5]

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)


models={
        "LinearRegression":LinearRegression(),
        "RidgeRegression":Ridge(),
        "LassoRegression":Lasso(),
        "ElesticNetRegression":ElasticNet(),
        "SGDRegression":SGDRegressor(),
        "HuberReression":HuberRegressor(),
        "PolynomialRegression": Pipeline([
           ('poly',PolynomialFeatures(degree=4)),
           ('LinearRegression',LinearRegression())]),
        "SVR":SVR(),
        "KNeighborsRegression":KNeighborsRegressor(),
        "RandomForestRegression":RandomForestRegressor(),
        "MLPRegression":MLPRegressor(),
        "xgboostRegression":xgb.XGBRegressor(),
        "lightgbmRegression":lgb.LGBMRegressor()
        }

result=[]

for name,model in models.items():
    model.fit(X_train,y_train)
    y_pred=model.predict(X_test)

    mae= mean_absolute_error(y_test, y_pred)
    mse= mean_squared_error(y_test, y_pred)
    r2= r2_score(y_test, y_pred)
    
    result.append({
        "model":name,
        'MSE':mse,
        'MAE':mae,
        'R2':r2
        })
    with open (f'{name}.pkl','wb')as f:
        pickle.dump(model,f)
        
result_df=pd.DataFrame(result)
result_df.to_csv('model evaluation.csv',index=False)        

print('code is pickle and save and the model evalution csv file is also save ')
        