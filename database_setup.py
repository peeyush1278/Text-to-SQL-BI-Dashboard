import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

def create_database():
    print("🛒 Building highly-realistic mock E-commerce Database...")
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # 1. Create Customers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        country TEXT,
        signup_date DATE
    )
    ''')

    # 2. Create Products Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL
    )
    ''')

    # 3. Create Sales Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        sale_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        sale_date DATE,
        quantity INTEGER,
        total_amount REAL,
        FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
        FOREIGN KEY (product_id) REFERENCES Products (product_id)
    )
    ''')
    
    # --- Populating Data ---
    
    # Products
    products = [
        (1, 'Wireless Mouse', 'Electronics', 25.99),
        (2, 'Mechanical Keyboard', 'Electronics', 89.50),
        (3, 'Gaming Monitor', 'Electronics', 299.00),
        (4, 'Ergonomic Chair', 'Furniture', 149.99),
        (5, 'Standing Desk', 'Furniture', 450.00),
        (6, 'Noise Cancelling Headphones', 'Electronics', 199.99),
        (7, 'Coffee Mug', 'Kitchen', 12.50),
        (8, 'Desk Lamp', 'Office Supplies', 34.00)
    ]
    cursor.executemany("INSERT OR REPLACE INTO Products VALUES (?, ?, ?, ?)", products)

    # Customers
    countries = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'India']
    customers = []
    for i in range(1, 101):
        signup_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))
        customers.append((i, f"Customer_{i}", f"cust{i}@example.com", random.choice(countries), signup_date.strftime('%Y-%m-%d')))
    cursor.executemany("INSERT OR REPLACE INTO Customers VALUES (?, ?, ?, ?, ?)", customers)

    # Sales
    sales = []
    sale_id = 1
    for _ in range(300): # Generate 300 random sales
        customer_id = random.randint(1, 100)
        product_idx = random.randint(0, len(products)-1)
        product_id = products[product_idx][0]
        price = products[product_idx][3]
        
        quantity = random.randint(1, 3)
        total_amount = round(price * quantity, 2)
        
        # Sales between Dec 2025 and March 2026
        sale_date = datetime(2025, 12, 1) + timedelta(days=random.randint(0, 110))
        
        sales.append((sale_id, customer_id, product_id, sale_date.strftime('%Y-%m-%d'), quantity, total_amount))
        sale_id += 1
        
    cursor.executemany("INSERT OR REPLACE INTO Sales VALUES (?, ?, ?, ?, ?, ?)", sales)

    conn.commit()
    conn.close()
    print("✅ Database 'ecommerce.db' created successfully with 3 tables (Customers, Products, Sales).")

if __name__ == "__main__":
    create_database()
