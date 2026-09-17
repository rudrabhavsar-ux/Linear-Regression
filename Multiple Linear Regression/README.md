# Multiple Linear Regression — Economic Index Prediction

A project that fits a multiple linear regression model to predict a stock market **index price** from **interest rate** and **unemployment rate**, using scikit-learn.

## Overview

The script (`main.py`) walks through a complete multiple regression workflow:

1. Load `economic_index.csv`, drop the unneeded `Unnamed: 0`, `month`, and `year` columns, and visualize relationships between features with a Seaborn pairplot.
2. Split the data into input features (`interest_rate`, `unemployment_rate`) and target (`index_price`), then into training (75%) and testing (25%) sets.
3. Standardize the input features using `StandardScaler` — fit on training data, then apply the same transform to test data.
4. Fit a `LinearRegression` model on the training set and print the learned coefficients and intercept.
5. Run 3-fold cross-validation on the training set to sanity-check the model before touching the test set.
6. Predict on the test set and evaluate using MAE, MSE, RMSE, R², and Adjusted R².
7. Check regression assumptions visually: predicted vs. actual scatter, residual distribution (KDE), and residuals vs. predicted values.

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

`economic_index.csv` should be in the same directory as `main.py`, with the following columns:

| Column | Description |
|---|---|
| Unnamed: 0 | Row index (dropped before modeling) |
| year | Year of observation (dropped before modeling) |
| month | Month of observation (dropped before modeling) |
| interest_rate | Interest rate (%) — input feature |
| unemployment_rate | Unemployment rate (%) — input feature |
| index_price | Stock/economic index value — target |

## Usage

```bash
python main.py
```

Running it will:
- Display a pairplot of `interest_rate`, `unemployment_rate`, and `index_price`
- Print the model's coefficients and intercept
- Print 3-fold cross-validation scores (negative MSE — sklearn's convention, so higher/less-negative is better)
- Print test-set evaluation metrics (MSE, MAE, RMSE, R², Adjusted R²)
- Print the raw residuals for the test set
- Display three diagnostic plots: predicted vs. actual, residual distribution, and residuals vs. predicted

## Example Output

```
Coefficient : [ 2.1  -3.4 ] & Intercept : 1120.5
Validation Score :  [-1523.2 -1487.9 -1601.3]
Mean Squared Error :  1456.7
Mean Absolute Error :  30.2
Root Mean Squared Error :  38.2
R2 Score :  0.71
Adjusted R2 Score :  0.68
```

*(Exact values will vary depending on the dataset, split, and random state.)*

## Notes

- **Scaling**: `fit_transform` is applied only to `X_train`; `X_test` uses `transform` with the statistics learned from training, to avoid data leakage.
- **Cross-validation**: `cross_val_score` refits the model internally per fold, so it's unaffected by the earlier `.fit()` call on the full training set — it's a good way to gauge how stable the model is before evaluating on the held-out test set.
- **Adjusted R²** accounts for the number of predictors (2 in this case), which matters more as you add features — it penalizes adding predictors that don't meaningfully improve the fit.
- **Residual diagnostics** help verify key linear regression assumptions: residuals should be roughly normally distributed (KDE plot) and show no clear pattern when plotted against predictions (homoscedasticity check).
- Fix the stray `from statistics import LinearRegression` import at the top — it's overwritten by the correct `from sklearn.linear_model import LinearRegression` import below it, but it's dead code that should be removed.

## Possible Next Steps

- Check for multicollinearity between `interest_rate` and `unemployment_rate` using VIF (Variance Inflation Factor).
- Try regularized regression (Ridge/Lasso) if multicollinearity or overfitting is a concern.
- Bring back `year`/`month` as engineered features (e.g., time trend) instead of dropping them outright.
- Save the trained model and scaler with `joblib` for reuse without retraining.