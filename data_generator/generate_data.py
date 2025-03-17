import psycopg2
from psycopg2 import sql
from faker import Faker
import random
from datetime import datetime, timedelta
from config import DB_CONFIG

# Инициализация Faker
faker = Faker()

# Подключение к базе данных
def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Подключение к базе данных установлено.")
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        exit(1)

# Генерация данных для таблицы Users
def generate_users(cursor, count=100):
    for i in range(count):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        phone = faker.phone_number()
        registration_date = faker.date_between(start_date="-2y", end_date="today")
        loyalty_status = random.choice(["Gold", "Silver", "Bronze"])

        cursor.execute("""
            INSERT INTO Users (first_name, last_name, email, phone, registration_date, loyalty_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, registration_date, loyalty_status))

# Генерация данных для таблицы ProductCategories
def generate_categories(cursor, count=10):
    category_ids = []

    # Генерация категорий без родительской категории
    for _ in range(count):
        name = faker.word().capitalize()
        cursor.execute("""
            INSERT INTO ProductCategories (name, parent_category_id)
            VALUES (%s, NULL) RETURNING category_id
        """, (name,))
        category_ids.append(cursor.fetchone()[0])  # Сохраняем созданные category_id

    # Обновление части категорий для добавления родительской категории
    for category_id in category_ids:
        # С вероятностью 50% добавляем родительскую категорию
        if random.random() > 0.5:
            parent_category_id = random.choice(category_ids)
            if parent_category_id != category_id:  # Избегаем самоссылки
                cursor.execute("""
                    UPDATE ProductCategories
                    SET parent_category_id = %s
                    WHERE category_id = %s
                """, (parent_category_id, category_id))

# Генерация данных для таблицы Products
def generate_products(cursor, count=50):
    for _ in range(count):
        name = faker.word().capitalize()
        description = faker.sentence()
        category_id = random.randint(1, 10)  # У нас 10 категорий
        price = round(random.uniform(10, 100), 2)
        stock_quantity = random.randint(0, 1000)
        creation_date = faker.date_between(start_date="-1y", end_date="today")
        cursor.execute("""
            INSERT INTO Products (name, description, category_id, price, stock_quantity, creation_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, description, category_id, price, stock_quantity, creation_date))

# Генерация данных для таблицы Orders и OrderDetails
def generate_orders_and_details(cursor, user_count=100, product_count=50, order_count=200):
    for _ in range(order_count):
        user_id = random.randint(1, user_count)
        order_date = faker.date_time_between(start_date="-1y", end_date="now")
        total_amount = 0
        status = random.choice(["Pending", "Completed", "Cancelled"])
        delivery_date = order_date + timedelta(days=random.randint(1, 14)) if status == "Completed" else None

        cursor.execute("""
            INSERT INTO Orders (user_id, order_date, total_amount, status, delivery_date)
            VALUES (%s, %s, %s, %s, %s) RETURNING order_id
        """, (user_id, order_date, total_amount, status, delivery_date))
        order_id = cursor.fetchone()[0]

        # Генерация деталей заказа
        for _ in range(random.randint(1, 5)):  # До 5 товаров на заказ
            product_id = random.randint(1, product_count)
            quantity = random.randint(1, 10)
            cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
            price_per_unit = cursor.fetchone()[0]
            total_price = round(price_per_unit * quantity, 2)
            total_amount += total_price

            cursor.execute("""
                INSERT INTO OrderDetails (order_id, product_id, quantity, price_per_unit, total_price)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, product_id, quantity, price_per_unit, total_price))

        # Обновление общей суммы заказа
        cursor.execute("UPDATE Orders SET total_amount = %s WHERE order_id = %s", (total_amount, order_id))

# Основная функция
def main():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        print("Начинаем генерацию данных...")


        print("Генерация пользователей...")
        generate_users(cursor, count=100)

        print("Генерация категорий товаров...")
        generate_categories(cursor, count=10)

        print("Генерация товаров...")
        generate_products(cursor, count=50)

        print("Генерация заказов и деталей заказов...")
        generate_orders_and_details(cursor, user_count=100, product_count=50, order_count=200)

        conn.commit()
        print("Генерация данных завершена.")

    except Exception as e:
        print(f"Ошибка во время генерации данных: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
        print("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    main()
