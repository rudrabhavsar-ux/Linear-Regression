# Personal Finance Tracker

A personal finance tracker with a Flask backend for data entry (CRUD)
and a Streamlit dashboard for interactive analysis. Both apps read and
write the same SQLite database through a shared `database/` package.

## Features

- Add, edit, delete transactions with server-side validation
- Manage categories (income/expense)
- Set monthly budgets per category, with progress tracking
- Recurring transactions (weekly/monthly), run on demand
- CSV export and import
- pandas-powered analysis: monthly summaries, spend by category,
  top categories, running balance over time
- Static charts (matplotlib/seaborn) embedded in the Flask app
- Interactive Streamlit dashboard with date/category/type filters

## Project structure

```
personal_financial_tracker/
├── database/          # SQLite access layer (shared by both apps)
│   ├── db.py           # connection helper
│   ├── categories.py
│   ├── transactions.py
│   ├── budgets.py
│   └── recurring.py
├── analytics/          # pandas analysis + chart generation
│   ├── analysis.py
│   └── visuals.py
├── backend/             # Flask app (data entry / CRUD)
│   ├── app.py
│   ├── static/charts/    # generated PNGs (not committed)
│   └── templates/
└── dashboard/            # Streamlit app (analysis / viewing)
    └── dashboard.py
```

`database/Personal.db` is created automatically the first time you run
the setup commands below. Its location is resolved from `db.py`'s own
file path, so both the Flask app and the Streamlit dashboard always
read/write the same file no matter where you launch them from.

## Setup

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Initialize the database

Run these once, in order, from the project root:

```bash
python -m database.categories   # creates + seeds default categories
python -m database.transactions # creates the transactions table
python -m database.budgets      # creates the budgets table
python -m database.recurring    # creates the recurring table
```

Each script is safe to re-run (`CREATE TABLE IF NOT EXISTS`, and
category seeding uses `INSERT OR IGNORE`).

## Running the Flask app (data entry)

```bash
cd backend
python app.py
```

Visit `http://127.0.0.1:5000`. From here you can add/edit/delete
transactions, manage categories, set budgets, configure recurring
transactions, and import/export CSVs.

## Running the Streamlit dashboard (analysis)

```bash
streamlit run dashboard/dashboard.py
```

Run this from the project root (or anywhere — it adds the project
root to `sys.path` itself). Use the sidebar to filter by date range,
category, and transaction type; every chart and metric on the page
reacts to the filters.

Run both apps at the same time in separate terminals if you want to
add data in Flask and immediately see it reflected in Streamlit
(refresh the Streamlit page to pick up new data).

## CSV import format

When importing via the Flask `/import` page, the CSV must contain
these columns:

```
amount, type, category_id, date
```

`note` is optional. `category_id` must match an existing category's
ID (see the Categories page in the Flask app).

## Notes on design decisions

- **Single-user**: no authentication, no `users` table.
- **Categories are a DB table**, not a hardcoded list, so they can be
  added/edited without touching code.
- **Flask handles all writes**; Streamlit is read-only by design —
  this was a deliberate choice to practice both frameworks rather
  than collapsing everything into one app.
- **Amounts are always stored positive**; the `type` column
  (`income`/`expense`) determines direction.
