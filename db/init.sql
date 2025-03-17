-- Создание таблиц
CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(30),
    registration_date DATE,
    loyalty_status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS ProductCategories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    parent_category_id INT REFERENCES ProductCategories(category_id)
);

CREATE TABLE IF NOT EXISTS Products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    category_id INT REFERENCES ProductCategories(category_id),
    price DECIMAL(10, 2),
    stock_quantity INT,
    creation_date DATE
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    order_date TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20),
    delivery_date DATE
);

CREATE TABLE IF NOT EXISTS OrderDetails (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id),
    product_id INT REFERENCES Products(product_id),
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    total_price DECIMAL(10, 2)
);
