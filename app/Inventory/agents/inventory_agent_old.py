from tools.inventory_tools import (
    get_product_stock,
    update_stock,
    record_sale,
    list_products
)


class InventoryAgent:

    def handle_query(self, query: str):

        query = query.lower()

        # List all products
        if "list" in query or "show products" in query:
            return list_products()

        # Check stock
        elif "stock" in query:

            product_name = query.replace("stock", "").strip()

            return get_product_stock(product_name)

        # Buy product
        elif "buy" in query:

            # Example:
            # "buy iphone 15 2"

            parts = query.split()

            try:
                quantity = int(parts[-1])
                product_name = " ".join(parts[1:-1])

                product = get_product_stock(product_name)

                if "error" in product:
                    return product

                return record_sale(product["id"], quantity)

            except Exception as e:
                return {"error": str(e)}

        return {"message": "Query not understood"}
    

agent = InventoryAgent()

print("\n--- LIST PRODUCTS ---")
print(agent.handle_query("list products"))

print("\n--- CHECK STOCK ---")
print(agent.handle_query("stock iphone 15"))

print("\n--- BUY PRODUCT ---")
print(agent.handle_query("buy iphone 15 2"))