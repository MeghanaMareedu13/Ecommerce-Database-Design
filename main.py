import sqlite3
import pandas as pd
import os

DB_NAME = "ecommerce.db"

def init_db():
    """Initializes the SQLite database with schema and seed data."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open("schema.sql", "r") as f:
        cursor.executescript(f.read())
    
    # Read and execute seed data
    with open("seed_data.sql", "r") as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()
    print(f"✅ Database '{DB_NAME}' initialized successfully.")

def run_analytics_queries():
    """Demonstrates SQL expertise with complex analytic queries."""
    conn = sqlite3.connect(DB_NAME)
    
    print("\n--- QUERY 1: Sales Summary (Joins & Aggregation) ---")
    query1 = """
    SELECT 
        u.first_name || ' ' || u.last_name as customer,
        o.order_id,
        o.total_amount,
        o.status,
        COUNT(oi.order_item_id) as items_ordered
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
    """
    df1 = pd.read_sql_query(query1, conn)
    print(df1)

    print("\n--- QUERY 2: High Value Products by Category ---")
    query2 = """
    SELECT 
        c.name as category,
        p.name as product,
        p.price
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    WHERE p.price > 100
    ORDER BY p.price DESC
    """
    df2 = pd.read_sql_query(query2, conn)
    print(df2)

    print("\n--- QUERY 3: Stock Levels Alert ---")
    query3 = """
    SELECT name, stock_quantity 
    FROM products 
    WHERE stock_quantity < 50
    """
    df3 = pd.read_sql_query(query3, conn)
    print(df3)

    conn.close()

if __name__ == "__main__":
    init_db()
    run_analytics_queries()
