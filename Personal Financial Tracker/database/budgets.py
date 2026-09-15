from .db import get_connection


def create_table():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL UNIQUE,
            monthly_limit REAL NOT NULL CHECK(monthly_limit > 0),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    con.commit()
    con.close()


def set_budget(category_id, monthly_limit):
    """Insert a new budget, or update the limit if one already exists for this category."""
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO budgets (category_id, monthly_limit)
        VALUES (?, ?)
        ON CONFLICT(category_id) DO UPDATE SET monthly_limit = excluded.monthly_limit
    """, (category_id, monthly_limit))
    con.commit()
    con.close()


def get_all():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT b.id, b.category_id, c.name AS category_name, b.monthly_limit
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
    """)
    rows = cursor.fetchall()
    con.close()
    return rows


if __name__ == "__main__":
    create_table()
    print(get_all())
