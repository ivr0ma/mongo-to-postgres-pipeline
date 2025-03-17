-- Создание базы данных
CREATE DATABASE IF NOT EXISTS project_replica;

USE project_replica;

-- Создание пользователя с настройкой аутентификации
CREATE USER IF NOT EXISTS 'replication_user'@'%' IDENTIFIED BY 'replication_password';

-- Изменение механизма аутентификации на mysql_native_password
ALTER USER 'replication_user'@'%' IDENTIFIED WITH mysql_native_password BY 'replication_password';

-- Назначение привилегий пользователю
GRANT ALL PRIVILEGES ON project_replica.* TO 'replication_user'@'%';

-- Применение привилегий
FLUSH PRIVILEGES;

-- Создание таблиц
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(30),
    registration_date DATE,
    loyalty_status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS ProductCategories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    parent_category_id INT,
    FOREIGN KEY (parent_category_id) REFERENCES ProductCategories(category_id)
);

CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    category_id INT,
    price DECIMAL(10, 2),
    stock_quantity INT,
    creation_date DATE,
    FOREIGN KEY (category_id) REFERENCES ProductCategories(category_id)
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20),
    delivery_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS OrderDetails (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
