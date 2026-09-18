import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline


# Generating a dataset to be polynomial

X = 6 * np.random.rand(100, 1) - 3  # generates 100 values between -3 and 3
y = 0.5 * X**2 + 1.5 * X + 2 + np.random.rand(100, 1)  # the eq for polynomials


#Plotting the base graph 

def plot_data(X, y):
    plt.scatter(X, y, color='red')
    plt.xlabel("X")
    plt.ylabel("y")
    plt.title("Raw Data")
    plt.show()


# Generating the model for Polynomial Rregression

def poly_degree(degree):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

    poly = PolynomialFeatures(degree=degree, include_bias=True)
    regression = LinearRegression()

    #connecting the Polynomial Features and Linear Regression model through pipeline
    poly_reg = Pipeline([
        ('Polynomial Features', poly),
        ('Linear Regression', regression)
    ])
    poly_reg.fit(X_train, y_train)

    y_pred = poly_reg.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Degree {degree} -> MSE: {mse:.4f}, R2: {r2:.4f}")

    # smooth curve for plotting, independent of test point order
    X_new = np.linspace(-3, 3, 200).reshape(200, 1)
    y_new = poly_reg.predict(X_new)

    plt.plot(X_new, y_new, 'r', label="Degree " + str(degree), linewidth=2)
    plt.plot(X_train, y_train, "b.", linewidth=3, label="Train")
    plt.plot(X_test, y_test, "g.", linewidth=3, label="Test")
    plt.legend(loc="upper left")
    plt.xlabel("X")
    plt.ylabel("y")
    plt.axis([-4, 4, 0, 10])
    plt.title(f"Polynomial Regression (Degree {degree})")
    plt.show()


if __name__ == '__main__':
    plot_data(X, y)
    poly_degree(int(input("Enter the degree : ")))