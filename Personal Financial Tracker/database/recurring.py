from .db import get_connection
from datetime import datetime, timedelta


def create_table():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurring(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            frequency TEXT NOT NULL CHECK(frequency IN ('weekly', 'monthly')),
            next_due_date DATE NOT NULL,
            note TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    con.commit()
    con.close()


def insert(category_id, amount, type_, frequency, next_due_date, note=""):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO recurring (category_id, amount, type, frequency, next_due_date, note)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (category_id, amount, type_, frequency, next_due_date, note))
    con.commit()
    con.close()


def get_all():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT r.id, r.category_id, c.name AS category_name, r.amount, r.type,
               r.frequency, r.next_due_date, r.note
        FROM recurring r
        JOIN categories c ON r.category_id = c.id
    """)
    rows = cursor.fetchall()
    con.close()
    return rows


def _advance_date(date_str, frequency):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if frequency == "weekly":
        date += timedelta(weeks=1)
    elif frequency == "monthly":
        # Naive month advance; caps day at 28 to sidestep month-length edge cases.
        month = date.month % 12 + 1
        year = date.year + (1 if date.month == 12 else 0)
        day = min(date.day, 28)
        date = date.replace(year=year, month=month, day=day)
    return date.strftime("%Y-%m-%d")


def run_due_recurring():
    """
    Inserts a real transaction for every recurring entry due today or earlier,
    then advances that entry's next_due_date. Returns how many were processed.
    """
    from . import transactions

    con = get_connection()
    cursor = con.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM recurring WHERE next_due_date <= ?", (today,))
    due = cursor.fetchall()
    con.close()

    for r in due:
        transactions.insert(r["amount"], r["type"], r["category_id"], r["next_due_date"], r["note"])
        new_date = _advance_date(r["next_due_date"], r["frequency"])

        con2 = get_connection()
        con2.execute("UPDATE recurring SET next_due_date = ? WHERE id = ?", (new_date, r["id"]))
        con2.commit()
        con2.close()

    return len(due)


if __name__ == "__main__":
    create_table()
    print(get_all())
