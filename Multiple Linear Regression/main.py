import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score


##Getting the data,removing unnecssary columns and plotting the graph

df=pd.read_csv('economic_index.csv')
df.drop(columns=['Unnamed: 0','month','year'],inplace=True)
sns.pairplot(df)
plt.show()
#df.corr()    ##Used to see the correlation between every column


#Test,Train Split

X=df.iloc[:,:-1]
y=df.iloc[:,-1]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=43)


#Standardization

Standard=StandardScaler()
X_train=Standard.fit_transform(X_train)
X_test=Standard.transform(X_test)


#Prediction Model

regression=LinearRegression(n_jobs=-1)
regression.fit(X_train,y_train)
print(f"Coefficient : {regression.coef_} & Intercept : {regression.intercept_}")


#Cross validation

validation_score=cross_val_score(regression,X_train,y_train,scoring='neg_mean_squared_error',cv=3) #scoring parameter can be selected from the documentation and cv is customizable
print("Validation Score : ",validation_score)

#Prediction for the test data 

y_pred=regression.predict(X_test)
mse=mean_squared_error(y_test,y_pred)
mae=mean_absolute_error(y_test,y_pred)
rmse=np.sqrt(mse)
score=r2_score(y_test,y_pred)
Adj_R2=1-(1-score)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)

print("Mean Squared Error : ",mse)
print("Mean Absolute Error : ",mae)
print("Root Mean Squared Error : ",rmse)
print("R2 Score : ",score)
print("Adjusted R2 Score : ",Adj_R2)


#Assumptions

plt.scatter(y_test,y_pred)
plt.show()
residuals=y_test-y_pred
print(residuals)
sns.displot(residuals,kind='kde')
plt.show()
plt.scatter(y_pred,residuals)
plt.show()