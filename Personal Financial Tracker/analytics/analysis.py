import pandas as pd
from database.db import get_connection

def get_transactions_df():
    con = get_connection()
    df = pd.read_sql_query("""
        SELECT t.id, t.amount, t.type, t.date, t.note, c.name AS category
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
    """, con)
    con.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

def monthly_summary(df):
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")
    summary = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
    # ensure both columns always exist even if one type has no data yet
    for col in ["income", "expense"]:
        if col not in summary.columns:
            summary[col] = 0

    summary["net"] = summary["income"] - summary["expense"]
    return summary

def spend_by_category(df, start_date=None, end_date=None):
    filtered = df[df["type"] == "expense"].copy()
    if start_date:
        filtered = filtered[filtered["date"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered["date"] <= pd.to_datetime(end_date)]

    result = filtered.groupby("category")["amount"].sum().sort_values(ascending=False)
    return result

def top_categories(df, n=5):
    expense_totals = df[df["type"] == "expense"].groupby("category")["amount"].sum()
    return expense_totals.sort_values(ascending=False).head(n)

def daily_trend(df):
    df = df.copy()
    df["signed_amount"] = df.apply(
        lambda row: row["amount"] if row["type"] == "income" else -row["amount"],
        axis=1
    )
    daily = df.groupby("date")["signed_amount"].sum().sort_index()
    daily_df = daily.to_frame(name="daily_net")
    daily_df["running_balance"] = daily_df["daily_net"].cumsum()
    return daily_df