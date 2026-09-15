import sys
import os

# Makes the project root importable (database/, analytics/) regardless of
# whether this script is launched from backend/ or elsewhere.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import io

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, Response

from database import transactions, categories, budgets, recurring
from database.transactions import validate_transaction
from analytics import analysis, visuals

app = Flask(__name__)


def _regenerate_charts():
    """Recomputes analysis + regenerates all chart PNGs. Called on every index load."""
    df = analysis.get_transactions_df()
    if df.empty:
        return
    spend = analysis.spend_by_category(df)
    summary = analysis.monthly_summary(df)
    top = analysis.top_categories(df)
    daily = analysis.daily_trend(df)

    visuals.plot_spend_by_category(spend)
    visuals.plot_monthly_summary(summary)
    visuals.plot_top_categories(top)
    visuals.plot_daily_trend(daily)


@app.route("/")
def index():
    all_transactions = transactions.get_all()
    _regenerate_charts()
    return render_template("index.html", transactions=all_transactions)


@app.route("/add", methods=["GET", "POST"])
def add():
    all_categories = categories.get_all()

    if request.method == "POST":
        amount = request.form.get("amount")
        type_ = request.form.get("type")
        category_id = request.form.get("category_id")
        date = request.form.get("date")
        note = request.form.get("note", "")

        errors = validate_transaction(amount, type_, category_id, date)
        if errors:
            return render_template("add.html", categories=all_categories, errors=errors)

        transactions.insert(float(amount), type_, int(category_id), date, note)
        return redirect(url_for("index"))

    return render_template("add.html", categories=all_categories, errors=None)


@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit(transaction_id):
    all_categories = categories.get_all()

    if request.method == "POST":
        amount = request.form.get("amount")
        type_ = request.form.get("type")
        category_id = request.form.get("category_id")
        date = request.form.get("date")
        note = request.form.get("note", "")

        errors = validate_transaction(amount, type_, category_id, date)
        if errors:
            transaction = transactions.get_by_id(transaction_id)
            return render_template("edit.html", transaction=transaction, categories=all_categories, errors=errors)

        transactions.update(transaction_id, float(amount), type_, int(category_id), date, note)
        return redirect(url_for("index"))

    transaction = transactions.get_by_id(transaction_id)
    return render_template("edit.html", transaction=transaction, categories=all_categories, errors=None)


@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete(transaction_id):
    transactions.delete(transaction_id)
    return redirect(url_for("index"))


# ---- Categories ----

@app.route("/categories")
def list_categories():
    return render_template("categories.html", categories=categories.get_all())


@app.route("/categories/add", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form["name"]
        type_ = request.form["type"]
        categories.insert(name, type_)
        return redirect(url_for("list_categories"))
    return render_template("add_category.html")


@app.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        name = request.form["name"]
        type_ = request.form["type"]
        categories.update(category_id, name, type_)
        return redirect(url_for("list_categories"))
    category = categories.get_by_id(category_id)
    return render_template("edit_category.html", category=category)


@app.route("/categories/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    categories.delete(category_id)
    return redirect(url_for("list_categories"))


# ---- Budgets ----

@app.route("/budgets", methods=["GET", "POST"])
def manage_budgets():
    if request.method == "POST":
        category_id = int(request.form["category_id"])
        monthly_limit = float(request.form["monthly_limit"])
        budgets.set_budget(category_id, monthly_limit)
        return redirect(url_for("manage_budgets"))

    return render_template("budgets.html", budgets=budgets.get_all(), categories=categories.get_all())


# ---- Recurring transactions ----

@app.route("/recurring", methods=["GET", "POST"])
def manage_recurring():
    if request.method == "POST":
        category_id = int(request.form["category_id"])
        amount = float(request.form["amount"])
        type_ = request.form["type"]
        frequency = request.form["frequency"]
        next_due_date = request.form["next_due_date"]
        note = request.form.get("note", "")
        recurring.insert(category_id, amount, type_, frequency, next_due_date, note)
        return redirect(url_for("manage_recurring"))

    return render_template("recurring.html", recurring=recurring.get_all(), categories=categories.get_all())


@app.route("/recurring/run", methods=["POST"])
def run_recurring():
    recurring.run_due_recurring()
    return redirect(url_for("index"))


# ---- CSV export / import ----

@app.route("/export")
def export_csv():
    all_transactions = transactions.get_all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "type", "category", "amount", "note"])
    for t in all_transactions:
        writer.writerow([t["date"], t["type"], t["category_name"], t["amount"], t["note"]])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=transactions.csv"}
    )


@app.route("/import", methods=["GET", "POST"])
def import_csv():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return render_template("import.html", error="No file selected.")

        try:
            df = pd.read_csv(file)
        except Exception:
            return render_template("import.html", error="Could not read that CSV file.")

        required_cols = {"amount", "type", "category_id", "date"}
        if not required_cols.issubset(df.columns):
            return render_template("import.html", error=f"CSV must contain columns: {sorted(required_cols)}")

        for _, row in df.iterrows():
            note = row.get("note", "") if pd.notna(row.get("note", "")) else ""
            transactions.insert(row["amount"], row["type"], int(row["category_id"]), row["date"], note)

        return redirect(url_for("index"))

    return render_template("import.html", error=None)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
