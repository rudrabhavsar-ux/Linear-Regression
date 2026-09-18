# Polynomial Regression — Degree Fitting on Synthetic Data

A project that generates a synthetic quadratic dataset and fits polynomial regression models of varying degree to it, using scikit-learn's `PolynomialFeatures` + `LinearRegression` combo inside a `Pipeline`.

## Overview

The script walks through a polynomial regression workflow:

1. Generate a synthetic dataset of 100 points where `X` ranges from -3 to 3, and `y` follows `y = 0.5x² + 1.5x + 2 + noise` — a quadratic relationship with a bit of random noise.
2. `plot_data()` — visualize the raw scatter of `X` vs `y` before any modeling.
3. `poly_degree(degree)` — for a given polynomial degree:
   - Splits the data into training (75%) and testing (25%) sets.
   - Expands `X` into polynomial features (e.g., for degree 2: `1, X, X²`) via `PolynomialFeatures`.
   - Fits a `LinearRegression` on the expanded features inside a `Pipeline`.
   - Evaluates the fit on the test set with MSE and R².
   - Plots the fitted curve over a smooth, independently generated range of `X` values (`X_new`), along with the actual train/test points.

## Requirements

- Python 3.x
- numpy
- pandas
- matplotlib
- scikit-learn

Install them with:

```bash
pip install numpy pandas matplotlib scikit-learn
```

## Usage

```bash
python main.py
```

Running it will:
- Display a scatter plot of the raw generated data
- Print `Degree {n} -> MSE: ..., R2: ...` for the tested degree
- Display a plot showing the fitted polynomial curve, training points (blue), and test points (green)

To try a different polynomial degree, call `poly_degree(<degree>)` with a different value in place of (or in addition to) `poly_degree(2)`.

## Key Design Notes

- **Why `X_new` instead of plotting `X_test` directly**: `train_test_split` shuffles the data, so `X_test` is in random order along the x-axis. Plotting `y_pred` against an unsorted `X_test` produces a jagged, zigzagging line instead of a smooth curve. Generating `X_new = np.linspace(-3, 3, 200).reshape(200, 1)` and predicting on that instead gives a clean curve showing the model's learned function across the full input range, independent of which points happened to land in the test set.
- **Pipeline**: Combining `PolynomialFeatures` and `LinearRegression` in a `Pipeline` means calling `.fit()` and `.predict()` once handles both the feature expansion and the regression — and it keeps the same transform consistently applied to any new data (like `X_new`) at prediction time.
- **`include_bias=True`**: Keeps the constant term (`1`) in the expanded feature set, which `LinearRegression` uses as part of its own intercept fitting. Fine here since features aren't standardized afterward.
- **Train/test split scope**: The split currently happens inside `poly_degree()`. If you plan to compare multiple degrees and want a fair, consistent comparison, do the split once outside the function and pass `X_train, X_test, y_train, y_test` in as arguments instead — otherwise each call gets a different random split.
- **No random seed**: `np.random.rand(...)` isn't seeded, so the dataset (and therefore the fit/metrics) will differ slightly on every run. Add `np.random.seed(<n>)` near the top if you want reproducible results across runs.

## Possible Next Steps

- Loop over multiple degrees (e.g., 1 through 10) and plot MSE/R² vs. degree to visualize underfitting vs. overfitting.
- Add regularization (Ridge/Lasso) for higher-degree fits to control overfitting.
- Refactor the split to happen once, outside `poly_degree()`, for consistent comparisons across degrees.
- Overlay multiple degree curves on the same plot for a direct visual comparison.