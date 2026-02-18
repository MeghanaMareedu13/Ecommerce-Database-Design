-- Seed Data for E-commerce Database

-- Categories
INSERT INTO categories (name, description) VALUES 
('Electronics', 'Gadgets and hardware'),
('Home & Kitchen', 'Appliances and decor'),
('Books', 'Physical and electronic books');

-- Products
INSERT INTO products (category_id, name, description, price, stock_quantity) VALUES 
(1, 'Laptop Pro 15', 'High-performance laptop for professionals', 1299.99, 50),
(1, 'Wireless Mouse', 'Ergonomic 2.4GHz mouse', 25.50, 200),
(2, 'Coffee Maker', 'Programmable 12-cup brewer', 79.99, 30),
(3, 'SQL Design Patterns', 'Advanced database modeling guide', 45.00, 100);

-- Users
INSERT INTO users (first_name, last_name, email, password_hash, address) VALUES 
('John', 'Doe', 'john.doe@example.com', 'hashed_pass_123', '123 Tech Lane, Austin, TX'),
('Jane', 'Smith', 'jane.smith@example.com', 'hashed_pass_456', '456 Data Drive, San Francisco, CA');

-- Orders
INSERT INTO orders (user_id, total_amount, status) VALUES 
(1, 1325.49, 'Delivered'),
(2, 45.00, 'Shipped');

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES 
(1, 1, 1, 1299.99),
(1, 2, 1, 25.50),
(2, 4, 1, 45.00);
