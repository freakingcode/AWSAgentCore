from tools.analytics_tools import (
    get_top_selling_products,
    get_low_stock_products,
    get_dead_stock_products,
    generate_restock_recommendations
)


class ProcurementAgent:

    def handle_query(self, query: str):

        query = query.lower()

        if "top selling" in query:
            return get_top_selling_products()

        elif "low stock" in query:
            return get_low_stock_products()

        elif "dead stock" in query:
            return get_dead_stock_products()

        elif "restock" in query:
            return generate_restock_recommendations()

        return {"message": "Query not understood"}