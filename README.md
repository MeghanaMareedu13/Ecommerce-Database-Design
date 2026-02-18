# 🗄️ Day 10: E-commerce Database Design

## 📝 Overview
This repository showcases a professional, normalized database schema designed for an E-commerce platform. It demonstrates advanced SQL concepts, including data modeling, referential integrity, indexing, and complex analytic queries.

## 🏗️ The Schema
The database follows **3rd Normal Form (3NF)** to ensure data integrity and minimize redundancy.

### Entity Relationship Diagram (ERD)
```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    CATEGORIES ||--|{ PRODUCTS : contains
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : "is in"

    USERS {
        int user_id PK
        string first_name
        string last_name
        string email UK
        string password_hash
        string address
        datetime created_at
    }

    CATEGORIES {
        int category_id PK
        string name UK
        string description
    }

    PRODUCTS {
        int product_id PK
        int category_id FK
        string name
        string description
        decimal price
        int stock_quantity
    }

    ORDERS {
        int order_id PK
        int user_id FK
        datetime order_date
        decimal total_amount
        string status
    }

    ORDER_ITEMS {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
```

## 🚀 Key Features
- **Normalization**: Structured into 5 optimized tables (Users, Products, Categories, Orders, OrderItems).
- **Indexing Strategy**: B-tree indexes on foreign keys to optimize Join performance.
- **Live Transaction Simulator**: A built-in engine that simulates real-time e-commerce orders.
- **Real-Time Analytics Dashboard**: A Streamlit interface that tracks revenue, order distribution, and stock levels as transactions occur.

## 🛠️ Tech Stack
- **Database Engine**: SQLite (SQL)
- **Dashboard**: Streamlit
- **Visualization**: Plotly
- **Scripting**: Python (Asyncio, Pandas)

## 🏃 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the live dashboard:
   ```bash
   streamlit run streamlit_app.py
   ```
3. Click **"Start Live Data Stream"** in the sidebar to begin the simulation.


---
*Developed as part of the 30-Day Recruiter Attraction Challenge.*
