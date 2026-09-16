import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

#plotting the graph for height and weight

df=pd.read_csv('height_weight.csv')
plt.scatter(df['weight'],df['height'])
plt.xlabel("Weight")
plt.ylabel("Height")
#sns.pairplot(df)  # Can use this Function as well
plt.show()


#Splitting the dataframe for training and testing

x=df[['weight']] #input features needs to be in 2D
y=df['height'] #output features can be in 1D
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=19) #splitting the test and train data


#Standardization

Standard=StandardScaler()
x_train=Standard.fit_transform(x_train)
x_test=Standard.transform(x_test)


#Prediction for the best fit line

regression=LinearRegression(n_jobs=-1)
regression.fit(x_train,y_train)
#print the coefficient(slope) and intercept
print(f"Coefficient : {regression.coef_} & Intercept : {regression.intercept_}")


#plotting the best fit line

plt.title("Predicted BestFit Line")
plt.scatter(x_train,y_train)
plt.plot(x_train,regression.predict(x_train))
plt.show()


#Prediction of test data

y_pred=regression.predict(x_test)


#calculating mse,mae,rmse,r2,adjusted r2


mae=mean_absolute_error(y_test,y_pred)
mse=mean_squared_error(y_test,y_pred)
rmse=np.sqrt(mse)
score=r2_score(y_test,y_pred)
Adj_R2=1-(1-score)*(len(y_test)-1)/(len(y_test)-x_test.shape[1]-1)

print("Mean Squared Error : ",mse)
print("Mean Absolute Error : ",mae)
print("Root Mean Squared Error : ",rmse)
print("R2 Score : ",score)
print("Adjusted R2 Score : ",Adj_R2)


#For new Prediction 
n=float(input("Enter Weight in Kgs : "))
print(f"Prediction for Height : {regression.predict(Standard.transform([[n]]))}")
