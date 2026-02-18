import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time
import random
import asyncio
from datetime import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="Live E-commerce DB Monitor", page_icon="🗄️", layout="wide")

# 2. Database Helpers
DB_NAME = "ecommerce.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        cursor = conn.cursor()
        with open("schema.sql", "r") as f:
            cursor.executescript(f.read())
        with open("seed_data.sql", "r") as f:
            cursor.executescript(f.read())
        conn.commit()
        conn.close()

# 3. Live Transaction Simulator
async def simulate_orders():
    """Background task to simulate live incoming orders."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get products and users for randomization
    cursor.execute("SELECT product_id, price FROM products")
    products = cursor.fetchall()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    while st.session_state.is_streaming:
        # Create a new random order
        user_id = random.choice(users)[0]
        # Pick 1-3 random products
        selected_items = random.sample(products, random.randint(1, 3))
        total_amount = sum(item[1] for item in selected_items)
        
        # Insert Order
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)",
            (user_id, total_amount, random.choice(['Pending', 'Shipped', 'Delivered']))
        )
        order_id = cursor.lastrowid
        
        # Insert Order Items
        for item in selected_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, item[0], 1, item[1])
            )
        
        conn.commit()
        st.session_state.last_transaction = f"New Order #{order_id} | Total: ${total_amount:.2f}"
        
        # Random delay between orders
        await asyncio.sleep(random.uniform(1.0, 3.0))

# 4. UI Layout
st.title("🗄️ Live E-commerce Database Engine")
st.markdown("Simulating enterprise-level database traffic with real-time ACID transactions.")

# Initialize state
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False
if 'last_transaction' not in st.session_state:
    st.session_state.last_transaction = "Waiting for stream..."

# Sidebar
with st.sidebar:
    st.header("⚙️ Control Panel")
    if not st.session_state.is_streaming:
        if st.button("🚀 Start Live Data Stream", type="primary", use_container_width=True):
            st.session_state.is_streaming = True
            st.rerun()
    else:
        if st.button("🛑 Stop Live Data Stream", use_container_width=True):
            st.session_state.is_streaming = False
            st.rerun()
            
    st.divider()
    st.info("System Status: " + ("🟢 ACTIVE" if st.session_state.is_streaming else "🔘 IDLE"))
    st.write(f"Last Event: {st.session_state.last_transaction}")

# Initialize DB
init_db()

# Dashboard UI
col1, col2, col3 = st.columns(3)
kpi1 = col1.empty()
kpi2 = col2.empty()
kpi3 = col3.empty()

chart_col1, chart_col2 = st.columns(2)
area_chart = chart_col1.empty()
pie_chart = chart_col2.empty()

log_header = st.subheader("📜 Recent Transactions (Live Query)")
log_table = st.empty()

async def run_dashboard():
    # Start simulator in background if streaming
    if st.session_state.is_streaming:
        asyncio.create_task(simulate_orders())
    
    conn = get_db_connection()
    
    while True:
        # 1. Fetch KPI Metrics
        total_sales = pd.read_sql_query("SELECT SUM(total_amount) as val FROM orders", conn).iloc[0]['val'] or 0
        order_count = pd.read_sql_query("SELECT COUNT(*) as val FROM orders", conn).iloc[0]['val']
        avg_value = total_sales / order_count if order_count > 0 else 0
        
        kpi1.metric("Total Revenue", f"${total_sales:,.2f}")
        kpi2.metric("Total Orders", f"{order_count}")
        kpi3.metric("Avg Order Value", f"${avg_value:.2f}")
        
        # 2. Category Performance
        df_cat = pd.read_sql_query("""
            SELECT c.name as Category, SUM(oi.quantity * oi.unit_price) as Revenue
            FROM categories c
            JOIN products p ON c.category_id = p.category_id
            JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY c.name
        """, conn)
        
        fig1 = px.bar(df_cat, x='Category', y='Revenue', title="Revenue by Category", template='plotly_dark', color='Category')
        area_chart.plotly_chart(fig1, use_container_width=True)
        
        # 3. Order Status Distro
        df_status = pd.read_sql_query("SELECT status, COUNT(*) as Count FROM orders GROUP BY status", conn)
        fig2 = px.pie(df_status, values='Count', names='status', title="Order Status Distribution", hole=0.4, template='plotly_dark')
        pie_chart.plotly_chart(fig2, use_container_width=True)
        
        # 4. Recent Transactions
        df_recent = pd.read_sql_query("""
            SELECT o.order_id as ID, u.first_name || ' ' || u.last_name as Customer, o.total_amount as Total, o.status as Status, o.order_date as Date
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            ORDER BY o.order_id DESC LIMIT 10
        """, conn)
        log_table.table(df_recent)
        
        if not st.session_state.is_streaming:
            break
            
        await asyncio.sleep(2)

if st.session_state.is_streaming or 'first_run' not in st.session_state:
    st.session_state.first_run = True
    asyncio.run(run_dashboard())
