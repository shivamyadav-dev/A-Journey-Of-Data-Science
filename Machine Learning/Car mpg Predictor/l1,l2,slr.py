import pandas as pd
import numpy as np


import seaborn as sns 
import matplotlib.pyplot as plt
#%matplotlib inline

from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression,Ridge,Lasso 
from sklearn.metrics import r2_score


data=pd.read_csv(r"C:\Users\Shivam Kumar yadav\OneDrive\Desktop\FSDS\Machine Learning (ML)\class notes\03_Regularization (L1,L2)\car-mpg.csv")
data.head()

#Drop car name 
data=data.drop(['car_name'],axis=1)

#Replace origin into 1,2,3..  dont forget get_dummies
data['origin']=data['origin'].replace({1:'america',2:'europe',3:'asia'})
data=pd.get_dummies(data,columns=['origin'],dtype=int)

data=data.replace('?',np.nan)
data['hp']=data['hp'].astype(float)
data=data.apply(lambda x:x.fillna(x.median()),axis=0)

data.head()

#print(data.dtypes)
#data['hp'] = pd.to_numeric(data['hp'], errors='coerce')
#data = data.fillna(data.median(numeric_only=True))



X=data.drop(['mpg'],axis=1)
y=data[['mpg']]


#Scaling the data 
X_s = preprocessing.scale(X)
X_s = pd.DataFrame(X_s,columns=X.columns)

y_s = preprocessing.scale(y)
y_s = pd.DataFrame(y_s,columns=y.columns)


#Split into train , test set

X_train,X_test,y_train,y_test=train_test_split(X_s,y_s,test_size=0.30,random_state=1)
X_train.shape

#Fit simple linear model and find coefficients

regression_model=LinearRegression()
regression_model.fit(X_train,y_train)

for idx,col_name in enumerate(X_train.columns):
    print('The cofficient for {} is {}'.format(col_name,regression_model.coef_[0][idx]))

intercept=regression_model.intercept_[0]
print('The intercept is {}'.format(intercept))


#Ridge Regression 

ridge_model=Ridge(alpha=0.3)
ridge_model.fit(X_train,y_train)

print('Ridge model coef:{}'.format(ridge_model.coef_))


#Regularized Lasso Regression 

lasso_model=Lasso(alpha=0.1)
lasso_model.fit(X_train,y_train)

print('Lasso model coef:{}'.format(lasso_model.coef_))

#Score Comparision

# Simple Linear Model 
print(regression_model.score(X_train,y_train))
print(regression_model.score(X_test,y_test))
print('*************************')

#Ridge
print(ridge_model.score(X_train,y_train))
print(ridge_model.score(X_test,y_test))
print('*************************')

#Lasso
print(lasso_model.score(X_train,y_train))
print(lasso_model.score(X_test,y_test))


#Polynomial Features

poly = PolynomialFeatures(degree = 2, interaction_only = True)
X_poly=poly.fit_transform(X_s)


#Model  parameter Tuning 

data_train_test=pd.concat([X_train,y_train],axis=1)
data_train_test.head()

import statsmodels.formula.api as smf
ols1=smf.ols(formula='mpg~cyl+disp+hp+acc+yr+car_type+origin_america+origin_europe+origin_asia',data=data_train_test).fit()
ols1.params

print(ols1.summary())

#Check Error

mse =np.mean((regression_model.predict(X_test)-y_test)**2)

import math
rmse=math.sqrt(mse)
print('Root Mean Squared Error:{}'.format(rmse))

#Graphical Representation

fig = plt.figure(figsize=(10,8))
sns.residplot(x= X_test['hp'], y= y_test['mpg'], color='green', lowess=True )


fig = plt.figure(figsize=(10,8))
sns.residplot(x= X_test['acc'], y= y_test['mpg'], color='green', lowess=True )



y_pred = regression_model.predict(X_test)
plt.scatter(y_test['mpg'], y_pred)
