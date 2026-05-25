# from agents.inventory_agent import InventoryAgent


# agent = InventoryAgent()

# print("\n--- LIST PRODUCTS ---")
# print(agent.handle_query("list products"))

# print("\n--- CHECK STOCK ---")
# print(agent.handle_query("stock iphone 15"))

# print("\n--- BUY PRODUCT ---")
# print(agent.handle_query("buy iphone 15 2"))


from agents.procurement_agent import ProcurementAgent

agent = ProcurementAgent()

print("\n--- TOP SELLING ---")
print(agent.handle_query("top selling"))

print("\n--- LOW STOCK ---")
print(agent.handle_query("low stock"))

print("\n--- DEAD STOCK ---")
print(agent.handle_query("dead stock"))

print("\n--- RESTOCK ---")
print(agent.handle_query("restock recommendations"))