


💰 Personal Financial Tracker
A simple personal finance tracking application built with Python, Flask, SQLite, Pandas, NumPy, and Matplotlib.

The project helps users record and manage financial transactions while providing analytical insights through charts and visualizations.

🚀 Features
Add financial transactions

Edit existing transactions

View transaction history

Categorize transactions

Track income and expenses

Analyze spending patterns

Generate financial visualizations

View daily spending trends

View monthly summaries

Analyze spending by category

Identify top spending categories

Store transaction data using SQLite

🛠️ Technologies Used
Python — Core programming language

Flask — Web application backend

SQLite3 — Local database

Pandas — Data analysis

NumPy — Numerical operations

Matplotlib — Data visualization

HTML/CSS — Frontend

📂 Project Structure
Personal Financial Tracker/
│
├── analytics/
│   ├── analysis.py
│   └── visuals.py
│
├── backend/
│   ├── static/
│   ├── templates/
│   │   ├── add.html
│   │   ├── edit.html
│   │   └── index.html
│   ├── __init__.py
│   └── app.py
│
├── database/
│   ├── __init__.py
│   ├── categories.py
│   ├── db.py
│   └── transactions.py
│
├── static/
│   └── charts/
│
├── .gitignore
├── README.md
└── requirements.txt
⚙️ Installation
1. Clone the repository
git clone <your-repository-url>
cd "Personal Financial Tracker"
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
▶️ Running the Application
Start the Flask application:

python backend/app.py
Then open:

http://127.0.0.1:5000/
in your browser.

📊 Analytics
The analytics module handles transaction analysis and visualization.

The project currently includes visualizations for:

Daily spending trends

Monthly financial summaries

Spending by category

Top spending categories

🗄️ Database
The application uses SQLite3 to store financial transaction data.

The local database file is intentionally excluded from the GitHub repository because it may contain personal financial information.

🔒 Privacy
Do not commit personal financial data or secrets to the repository.

The .gitignore file excludes:

SQLite database files

Python cache files

Virtual environments

Environment variables

Generated chart images

IDE and operating-system files

🔮 Future Improvements
Some possible improvements for the project include:

User authentication

Multiple user accounts

Budget tracking

Savings goals

Recurring transactions

CSV export

Interactive dashboards

More advanced financial analytics

Monthly financial reports

Cloud deployment

👨‍💻 Author
Rudra Bhavsar

Built as a personal finance tracking project using Python and Flask.