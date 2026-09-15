import sys
import os

# Makes the project root importable (database/, analytics/) regardless of
# whether this script is launched from dashboard/ or elsewhere.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from analytics import analysis
from database import categories
from database import budgets as budgets_db

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("Personal Finance Dashboard")

# ---- Load data ----
df = analysis.get_transactions_df()

if df.empty:
    st.warning("No transactions found. Add some via the Flask app first.")
    st.stop()

# ---- Sidebar filters ----
st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

all_categories = [c["name"] for c in categories.get_all()]
selected_categories = st.sidebar.multiselect(
    "Categories",
    options=all_categories,
    default=all_categories
)

selected_types = st.sidebar.multiselect(
    "Type",
    options=["income", "expense"],
    default=["income", "expense"]
)

# ---- Apply filters ----
start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)

filtered_df = df[
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date)) &
    (df["category"].isin(selected_categories)) &
    (df["type"].isin(selected_types))
]

if filtered_df.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

# ---- Summary metrics ----
total_income = filtered_df[filtered_df["type"] == "income"]["amount"].sum()
total_expense = filtered_df[filtered_df["type"] == "expense"]["amount"].sum()
net = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{total_income:,.2f}")
col2.metric("Total Expense", f"₹{total_expense:,.2f}")
col3.metric("Net Savings", f"₹{net:,.2f}")

st.divider()

# ---- Spend by category ----
st.subheader("Spending by Category")
spend = analysis.spend_by_category(filtered_df)

if not spend.empty:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=spend.index, y=spend.values, hue=spend.index, legend=False, palette="viridis", ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("No expense data in this range.")

# ---- Monthly income vs expense ----
st.subheader("Monthly Income vs Expense")
summary = analysis.monthly_summary(filtered_df)

fig, ax = plt.subplots(figsize=(9, 4))
x = summary.index.astype(str)
ax.plot(x, summary["income"], marker="o", label="Income")
ax.plot(x, summary["expense"], marker="o", label="Expense")
ax.set_xlabel("Month")
ax.set_ylabel("Amount")
ax.legend()
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)

# ---- Balance over time ----
st.subheader("Balance Over Time")
daily = analysis.daily_trend(filtered_df)

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(daily.index, daily["running_balance"])
ax.set_xlabel("Date")
ax.set_ylabel("Running Balance")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)

# ---- Budget status (current month) ----
st.subheader("Budget Status (This Month)")
spend_this_month = analysis.current_month_spend_by_category(df)
all_budgets = budgets_db.get_all()

if not all_budgets:
    st.info("No budgets set yet. Set them from the Flask app's Budgets page.")
else:
    for b in all_budgets:
        spent = spend_this_month.get(b["category_name"], 0)
        limit = b["monthly_limit"]
        pct = min(spent / limit, 1.0) if limit > 0 else 0
        st.write(f"**{b['category_name']}**: ₹{spent:,.2f} / ₹{limit:,.2f}")
        st.progress(pct)

# ---- Raw data ----
with st.expander("View all transactions"):
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download as CSV", data=csv, file_name="transactions.csv", mime="text/csv")
