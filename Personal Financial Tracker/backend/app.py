from flask import Flask, render_template, request, redirect, url_for
from database import transactions, categories
from analytics import analysis
from analytics import visuals

app = Flask(__name__)

@app.route("/")
def index():
    all_transactions = transactions.get_all()

    df = analysis.get_transactions_df()
    if not df.empty:
        spend = analysis.spend_by_category(df)
        summary = analysis.monthly_summary(df)
        top = analysis.top_categories(df)
        daily = analysis.daily_trend(df)

        visuals.plot_spend_by_category(spend)
        visuals.plot_monthly_summary(summary)
        visuals.plot_top_categories(top)
        visuals.plot_daily_trend(daily)

    return render_template("index.html", transactions=all_transactions)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        amount = request.form["amount"]
        type_ = request.form["type"]
        category_id = request.form["category_id"]
        date = request.form["date"]
        note = request.form.get("note", "")

        transactions.insert(amount, type_, category_id, date, note)
        return redirect(url_for("index"))

    all_categories = categories.get_all()
    return render_template("add.html", categories=all_categories)

@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit(transaction_id):
    if request.method == "POST":
        amount = request.form["amount"]
        type_ = request.form["type"]
        category_id = request.form["category_id"]
        date = request.form["date"]
        note = request.form.get("note", "")

        transactions.update(transaction_id, amount, type_, category_id, date, note)
        return redirect(url_for("index"))

    transaction = transactions.get_by_id(transaction_id)
    all_categories = categories.get_all()
    return render_template("edit.html", transaction=transaction, categories=all_categories)

@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete(transaction_id):
    transactions.delete(transaction_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)