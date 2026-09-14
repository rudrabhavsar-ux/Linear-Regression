from .db import get_connection

def create_table():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
        )
    """)
    con.commit()
    con.close()

def seed_categories():
    con = get_connection()
    cursor = con.cursor()
    default_categories = [
        ("Salary", "income"),
        ("Freelance", "income"),
        ("Food", "expense"),
        ("Rent", "expense"),
        ("Transport", "expense"),
        ("Entertainment", "expense"),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO categories (name, type)
        VALUES (?, ?)
    """, default_categories)
    con.commit()
    con.close()

def get_all():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT id, name, type FROM categories")
    rows = cursor.fetchall()
    con.close()
    return rows

def get_by_id(category_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT id, name, type FROM categories WHERE id = ?", (category_id,))
    row = cursor.fetchone()
    con.close()
    return row

if __name__ == "__main__":
    create_table()
    seed_categories()
    #print(get_all())