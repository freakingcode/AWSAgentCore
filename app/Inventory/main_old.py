from typing import Any
from unittest import result
from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model
from mcp_client.client import get_streamable_http_mcp_client
from tools.kb_tool import search_inventory_knowledge


from openai import OpenAI
from dotenv import load_dotenv
import os


app = BedrockAgentCoreApp()
log = app.logger

# Define a Streamable HTTP MCP Clien

DEFAULT_SYSTEM_PROMPT = """
You are an intelligent inventory assistant.

Use the knowledge base tool whenever inventory,
products, stock rules, SOPs, or documentation
questions are asked.
"""


# Define a collection of tools used by the model
tools = []
tools.append(search_inventory_knowledge)

# Define a simple function tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Return the sum of two numbers"""
    return a+b

tools.append(add_numbers)


# Add MCP client to tools if available
mcp_clients = [get_streamable_http_mcp_client()]

for mcp_client in mcp_clients:
    if mcp_client:
        tools.append(mcp_client)


_agent = None

def get_or_create_agent():
    global _agent
    if _agent is None:
        _agent = Agent(
            model=load_model(),
            system_prompt=DEFAULT_SYSTEM_PROMPT,
            tools=tools
        )
    return _agent


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Agent.....")

    agent = get_or_create_agent()

    # Execute and format response
    stream = agent.stream_async(payload.get("prompt"))

    async for event in stream:
        # Handle Text parts of the response
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]


# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# @app.entrypoint
# async def invoke(payload, context):

#     user_message = payload.get("prompt")

#     response = client.chat.completions.create(
#         model="gpt-4.1-mini",

#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are an inventory AI assistant."
#             },
#             {
#                 "role": "user",
#                 "content": user_message
#             }
#         ]
#     )

#     answer = response.choices[0].message.content

#     yield answer

if __name__ == "__main__":
    app.run()
