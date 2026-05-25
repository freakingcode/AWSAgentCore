import sqlite3
from pathlib import Path

# Database path
BASE_DIR = Path(__file__).resolve().parent.parent / "database"
DB_PATH = BASE_DIR / "inventory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# -----------------------------
# Get Product Stock
# -----------------------------
def get_product_stock(product_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, stock, price
        FROM products
        WHERE LOWER(name) = LOWER(?)
    """, (product_name,))

    product = cursor.fetchone()

    conn.close()

    if product:
        return {
            "id": product[0],
            "name": product[1],
            "stock": product[2],
            "price": product[3]
        }

    return {"error": "Product not found"}


# -----------------------------
# Update Stock
# -----------------------------
def update_stock(product_id: int, quantity: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Check current stock
    cursor.execute("""
        SELECT stock
        FROM products
        WHERE id = ?
    """, (product_id,))

    result = cursor.fetchone()

    if not result:
        conn.close()
        return {"error": "Product not found"}

    current_stock = result[0]
    new_stock = current_stock + quantity

    if new_stock < 0:
        conn.close()
        return {"error": "Insufficient stock"}

    # Update stock
    cursor.execute("""
        UPDATE products
        SET stock = ?
        WHERE id = ?
    """, (new_stock, product_id))

    conn.commit()
    conn.close()

    return {
        "message": "Stock updated successfully",
        "new_stock": new_stock
    }


# -----------------------------
# Record Sale
# -----------------------------
def record_sale(product_id: int, quantity: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch product details
    cursor.execute("""
        SELECT stock, price
        FROM products
        WHERE id = ?
    """, (product_id,))

    result = cursor.fetchone()

    if not result:
        conn.close()
        return {"error": "Product not found"}

    current_stock, price = result

    if current_stock < quantity:
        conn.close()
        return {"error": "Not enough stock available"}

    # Reduce stock
    new_stock = current_stock - quantity

    cursor.execute("""
        UPDATE products
        SET stock = ?
        WHERE id = ?
    """, (new_stock, product_id))

    # Insert sale record
    total_price = quantity * price

    cursor.execute("""
        INSERT INTO sales (product_id, quantity, total_price)
        VALUES (?, ?, ?)
    """, (product_id, quantity, total_price))

    conn.commit()
    conn.close()

    return {
        "message": "Sale recorded successfully",
        "remaining_stock": new_stock,
        "total_amount_of_sale": total_price
    }


# -----------------------------
# List Products
# -----------------------------
def list_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, stock, price
        FROM products
    """)

    products = cursor.fetchall()

    conn.close()

    return [
        {
            "id": p[0],
            "name": p[1],
            "category": p[2],
            "stock": p[3],
            "price": p[4]
        }
        for p in products
    ]



# print("\n--- LIST PRODUCTS ---")
# print(list_products())

# print("\n--- GET STOCK ---")
# print(get_product_stock("iPhone 15"))

# print("\n--- UPDATE STOCK ---")
# print(update_stock(1, 10))

# print("\n--- RECORD SALE ---")
# print(record_sale(1, 2))