import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../analytics
CHART_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "backend", "static", "charts"))

def _ensure_dir():
    os.makedirs(CHART_DIR, exist_ok=True)

def plot_spend_by_category(series, filename="spend_by_category.png"):
    _ensure_dir()
    path = os.path.join(CHART_DIR, filename)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=series.index, y=series.values, hue=series.index, legend=False, palette="viridis")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Spending by Category")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def plot_monthly_summary(summary_df, filename="monthly_summary.png"):
    _ensure_dir()
    path = os.path.join(CHART_DIR, filename)

    plt.figure(figsize=(9, 5))
    x = summary_df.index.astype(str)
    plt.plot(x, summary_df["income"], marker="o", label="Income")
    plt.plot(x, summary_df["expense"], marker="o", label="Expense")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Monthly Income vs Expense")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def plot_top_categories(series, filename="top_categories.png"):
    _ensure_dir()
    path = os.path.join(CHART_DIR, filename)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=series.values, y=series.index, hue=series.index, legend=False, palette="magma")
    plt.xlabel("Amount")
    plt.ylabel("Category")
    plt.title("Top Spending Categories")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def plot_daily_trend(daily_df, filename="daily_trend.png"):
    _ensure_dir()
    path = os.path.join(CHART_DIR, filename)

    plt.figure(figsize=(9, 5))
    plt.plot(daily_df.index, daily_df["running_balance"], marker=None)
    plt.xlabel("Date")
    plt.ylabel("Running Balance")
    plt.title("Balance Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

