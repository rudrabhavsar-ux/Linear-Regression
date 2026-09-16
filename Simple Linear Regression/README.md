# Simple Linear Regression — Weight vs Height

A beginner project that fits a simple linear regression model to predict **height** from **weight** using scikit-learn.

## Overview

The script (`main.py`) walks through a full, minimal ML workflow:

1. Load `height_weight.csv` and visualize the weight-height relationship with a scatter plot.
2. Split the data into training (75%) and testing (25%) sets.
3. Standardize the input feature (`weight`) using `StandardScaler`.
4. Fit a `LinearRegression` model and plot the resulting best-fit line.
5. Evaluate the model on the test set using MAE, MSE, RMSE, R², and Adjusted R².
6. Take a weight input from the user and predict the corresponding height.

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

Install them with:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## Dataset

`height_weight.csv` should be in the same directory as `main.py`, with two columns:

| Column | Description |
|--------|-------------|
| weight | Weight in kilograms (input feature) |
| height | Height in centimeters (target) |

## Usage

```bash
python main.py
```

The script will:
- Display a scatter plot of weight vs. height
- Print the model's coefficient (slope) and intercept
- Display a plot of the training data with the fitted regression line
- Print evaluation metrics on the test set
- Prompt you to enter a weight (in kg) and print the predicted height

## Example Output

```
Coefficient : [4.87] & Intercept : 165.32
Mean Squared Error :  8.42
Mean Absolute Error :  2.31
Root Mean Squared Error :  2.90
R2 Score :  0.61
Adjusted R2 Score :  0.59

Enter Weight in Kgs : 70
Prediction for Height : [167.91]
```

*(Exact values will vary depending on the dataset and train/test split.)*

## Notes

- The weight feature is standardized before fitting, so at prediction time the new input is also transformed with the same fitted `StandardScaler` before being passed to the model.
- `random_state=19` is used for the train/test split to make results reproducible.
- Adjusted R² accounts for the number of predictors, which matters more once you move to multiple linear regression.

## Possible Next Steps

- Add more features (e.g., age, gender) and extend to multiple linear regression.
- Try polynomial regression if the relationship isn't perfectly linear.
- Save/load the trained model with `joblib` or `pickle`.
- Add residual plots to check assumptions (linearity, homoscedasticity).