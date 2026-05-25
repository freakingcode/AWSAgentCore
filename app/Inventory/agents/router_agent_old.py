from agents.inventory_agent import InventoryAgent
from agents.procurement_agent import ProcurementAgent


class RouterAgent:

    def __init__(self):

        self.inventory_agent = InventoryAgent()
        self.procurement_agent = ProcurementAgent()

    def route_query(self, query: str):

        query = query.lower()

        # Procurement related queries
        procurement_keywords = [
            "top selling",
            "dead stock",
            "restock",
            "low stock",
            "demand",
            "analytics"
        ]

        # Inventory related queries
        inventory_keywords = [
            "buy",
            "stock",
            "inventory",
            "list products",
            "show products"
        ]

        # Route to Procurement Agent
        for keyword in procurement_keywords:
            if keyword in query:
                return self.procurement_agent.handle_query(query)

        # Route to Inventory Agent
        for keyword in inventory_keywords:
            if keyword in query:
                return self.inventory_agent.handle_query(query)

        return {
            "message": "Could not determine appropriate agent"
        }