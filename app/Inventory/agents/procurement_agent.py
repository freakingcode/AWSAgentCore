import json
import re

from utils.logger import logger
from services.bedrock_client import get_bedrock_client
from agents.tool_registry import PROCUREMENT_TOOLS
from tools.analytics_tools import (
    get_top_selling_products,
    get_low_stock_products,
    get_dead_stock_products,
    generate_restock_recommendations
)

class ProcurementAgent:

    def __init__(self):

        self.bedrock = get_bedrock_client()

    def decide_tool(self, query: str):

        prompt = f"""
You are an Inventory AI Agent.

Available tools:

1. get_top_selling_products()
   - Get top selling products

2. get_low_stock_products()
   - Get low stock products

3. get_dead_stock_products()
   - Get dead stock products

4. generate_restock_recommendations()
   - Generate restock recommendations based on current stock and sales data

Rules:
- Return ONLY valid JSON
- No explanation
- Use exact tool names

JSON format:
{{
    "tool": "tool_name",
    "arguments": {{
        "arg1": "value"
    }}
}}

User Query:
{query}
"""

        response = self.bedrock.invoke_model(
            modelId="amazon.nova-lite-v1:0",
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],

                "inferenceConfig": {
                    "maxTokens": 20,
                    "temperature": 0
                }

            })
        )

        # response_body = json.loads(response["body"].read())

        # print(response_body)

        # output = response_body["choices"][0]["message"]["content"]
        logger.info(f"Received response from Bedrock: {response}")
        response_body = json.loads(
            response["body"].read()
        )
        logger.info(f"Parsed response body: {response_body}")
        output = response_body["output"]["message"]["content"][0]["text"]
        logger.info("\n[RAW TOOL OUTPUT]:")
        logger.info(output)
        # print("\n[RAW TOOL OUTPUT]:")
        # print(output)

        # # Remove reasoning tags
        # clean_output = re.sub(
        #     r"<reasoning>.*?</reasoning>",
        #     "",
        #     output,
        #     flags=re.DOTALL
        # ).strip()

        # print("\n[CLEAN OUTPUT]:")
        # print(clean_output)

        return json.loads(output)

    def execute_tool(self, tool_name, arguments):

        if tool_name not in PROCUREMENT_TOOLS:
            return {
                "error": f"Unknown tool: {tool_name}"
            }

        tool = PROCUREMENT_TOOLS[tool_name]

        return tool(**arguments)

    def handle_query(self, query: str):
        logger.info("Executing procurement_agent.handle_query tool...")
        tool_decision = self.decide_tool(query)
        logger.info("\n[LLM Tool Decision]")
        logger.info(tool_decision)

        tool_name = tool_decision["tool"]
        arguments = tool_decision["arguments"]

        # Convert product_name → product_id
        if tool_name == "record_sale":

            product = get_product_stock(
                arguments["product_name"]
            )

            if "error" in product:
                return product

            arguments = {
                "product_id": product["id"],
                "quantity": arguments["quantity"]
            }

        return self.execute_tool(
            tool_name,
            arguments
        )