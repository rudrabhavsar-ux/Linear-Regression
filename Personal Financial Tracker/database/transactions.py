from .db import get_connection


def create_table():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            date DATE NOT NULL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    con.commit()
    con.close()


def validate_transaction(amount, type_, category_id, date):
    """Returns a list of human-readable error strings. Empty list = valid."""
    errors = []

    try:
        amount = float(amount)
        if amount <= 0:
            errors.append("Amount must be greater than 0.")
    except (ValueError, TypeError):
        errors.append("Amount must be a valid number.")

    if type_ not in ("income", "expense"):
        errors.append("Type must be 'income' or 'expense'.")

    try:
        int(category_id)
    except (ValueError, TypeError):
        errors.append("Invalid category.")

    if not date:
        errors.append("Date is required.")

    return errors


def get_all():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT t.id, t.amount, t.type, t.date, t.note, t.category_id, c.name AS category_name
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC
    """)
    rows = cursor.fetchall()
    con.close()
    return rows


def get_by_id(transaction_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT id, amount, type, date, note, category_id
        FROM transactions
        WHERE id = ?
    """, (transaction_id,))
    row = cursor.fetchone()
    con.close()
    return row


def insert(amount, type_, category_id, date, note=""):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO transactions (amount, type, category_id, date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (amount, type_, category_id, date, note))
    con.commit()
    con.close()


def update(transaction_id, amount, type_, category_id, date, note=""):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE transactions
        SET amount = ?, type = ?, category_id = ?, date = ?, note = ?
        WHERE id = ?
    """, (amount, type_, category_id, date, note, transaction_id))
    con.commit()
    con.close()


def delete(transaction_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    con.commit()
    con.close()


if __name__ == "__main__":
    create_table()
    print(get_all())
