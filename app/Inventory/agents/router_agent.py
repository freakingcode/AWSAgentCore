import json

from services.bedrock_client import get_bedrock_client

from agents.inventory_agent import InventoryAgent
from agents.procurement_agent import ProcurementAgent


class RouterAgent:

    def __init__(self):

        self.inventory_agent = InventoryAgent()
        self.procurement_agent = ProcurementAgent()

        self.bedrock = get_bedrock_client()

    def classify_intent(self, query: str):

        prompt = f"""
You are an intent classifier.

Classify the user query into ONLY one of these labels:

inventory
procurement

Rules:
- inventory → stock availability, product quantity, inventory status
- procurement → purchasing, supplier orders, restocking decisions

Return ONLY the label.
Do not explain.
Do not think step-by-step.
Do not include reasoning.
You MUST return one of the labels based on the query. Even if you are not sure, choose the most likely label. Do not return anything other than the label.

User Query:
{query}
"""

        response = self.bedrock.invoke_model(
            modelId="openai.gpt-oss-20b-1:0",
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_completion_tokens": 1000,
                "temperature": 0.5
            })
        )

        response_body = json.loads(response["body"].read())

        print(response_body)

        result = response_body["choices"][0]["message"]["content"]

        return result.strip().lower()

    def route_query(self, query: str):

        intent = self.classify_intent(query)

        print(f"\n[Router Decision]: {intent}")

        if "inventory" in intent:
            return self.inventory_agent.handle_query(query)

        elif "procurement" in intent:
            return self.procurement_agent.handle_query(query)

        return {
            "error": "Unable to determine intent"
        }