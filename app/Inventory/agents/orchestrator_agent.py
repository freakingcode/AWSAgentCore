import boto3
import json
import re
from agents.inventory_agent import InventoryAgent
from agents.procurement_agent import ProcurementAgent
from utils.logger import logger

class OrchestratorAgent:

    def __init__(self):

        self.inventory_agent = InventoryAgent()
        self.procurement_agent = ProcurementAgent()

        self.bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name="eu-north-1"
        )


    def classify_intent(self, query):
        logger.info("Classifying intent with Bedrock...")
        prompt = f"""
Classify the query into ONLY one label:

inventory
procurement

Rules:
- inventory = stock checks, products, inventory listing
- procurement = supplier orders, restocking, purchasing, top selling products, low stock products, dead stock products, restock recommendations, demand forecasting, analytics

Return ONLY the label.

Query:
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
        logger.info(f"Received response from Bedrock: {response}")
        response_body = json.loads(
            response["body"].read()
        )
        logger.info(f"Parsed response body: {response_body}")
        intent = response_body["output"]["message"]["content"][0]["text"]
        # intent = response_body["content"][0]["text"]
        logger.info(f"Extracted intent: {intent}")
        # clean_output = re.sub(
        #     r"<reasoning>.*?</reasoning>",
        #     "",
        #     intent,
        #     flags=re.DOTALL
        # ).strip()

        # logger.info("\n[CLEAN OUTPUT]:")
        # logger.info(clean_output)

        # return json.loads(clean_output)
        return intent.strip().lower()


    def route_query(self, query):
        logger.info("Executing orchestrator.route_query tool...")
        intent = self.classify_intent(query)
        logger.info(f"\n[Orchestrator Decision]: {intent}")

        if "inventory" in intent:

            return self.inventory_agent.handle_query(query)

        elif "procurement" in intent:

            return self.procurement_agent.handle_query(query)

        return {
            "error": "Unable to determine intent"
        }