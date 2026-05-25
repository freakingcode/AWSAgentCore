from tools.inventory_tools import (
    get_product_stock,
    update_stock,
    record_sale,
    list_products
)

from tools.analytics_tools import (
    get_top_selling_products,
    get_low_stock_products,
    get_dead_stock_products,
    generate_restock_recommendations
)

INVENTORY_TOOLS = {
    "get_product_stock": get_product_stock,
    "update_stock": update_stock,
    "record_sale": record_sale,
    "list_products": list_products
}

PROCUREMENT_TOOLS = {
    "get_top_selling_products": get_top_selling_products,
    "get_low_stock_products": get_low_stock_products,
    "get_dead_stock_products": get_dead_stock_products,
    "generate_restock_recommendations": generate_restock_recommendations
}