import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "database"
DB_PATH = BASE_DIR / "inventory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# -----------------------------------
# Top Selling Products
# -----------------------------------
def get_top_selling_products(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.name,
            SUM(s.quantity) as total_sold
        FROM sales s
        JOIN products p
        ON p.id = s.product_id
        GROUP BY p.name
        ORDER BY total_sold DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()

    conn.close()

    return [
        {
            "product": row[0],
            "total_sold": row[1]
        }
        for row in results
    ]


# -----------------------------------
# Low Stock Products
# -----------------------------------
def get_low_stock_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            stock,
            reorder_level
        FROM products
        WHERE stock < reorder_level
    """)

    results = cursor.fetchall()

    conn.close()

    return [
        {
            "product": row[0],
            "stock": row[1],
            "reorder_level": row[2]
        }
        for row in results
    ]


# -----------------------------------
# Dead Stock Products
# -----------------------------------
def get_dead_stock_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.name,
            p.stock
        FROM products p
        LEFT JOIN sales s
        ON p.id = s.product_id
        GROUP BY p.id
        HAVING COALESCE(SUM(s.quantity), 0) = 0
    """)

    results = cursor.fetchall()

    conn.close()

    return [
        {
            "product": row[0],
            "stock_remaining": row[1]
        }
        for row in results
    ]


# -----------------------------------
# Restock Recommendations
# -----------------------------------
def generate_restock_recommendations():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.name,
            p.stock,
            p.reorder_level,
            COALESCE(SUM(s.quantity), 0) as total_sales
        FROM products p
        LEFT JOIN sales s
        ON p.id = s.product_id
        GROUP BY p.id
    """)

    rows = cursor.fetchall()

    conn.close()

    recommendations = []

    for row in rows:

        name = row[0]
        stock = row[1]
        reorder_level = row[2]
        total_sales = row[3]

        if stock < reorder_level and total_sales > 5:
            recommendations.append({
                "product": name,
                "recommendation": "Restock immediately"
            })

        elif stock > 50 and total_sales == 0:
            recommendations.append({
                "product": name,
                "recommendation": "Potential dead stock"
            })

    return recommendations


print("\n--- LIST PRODUCTS ---")
print(get_top_selling_products())

print("\n--- GET STOCK ---")
print(get_low_stock_products())

print("\n--- UPDATE STOCK ---")
print(get_dead_stock_products())

print("\n--- RECORD SALE ---")
print(generate_restock_recommendations())