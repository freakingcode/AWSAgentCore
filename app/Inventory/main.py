from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from agents.orchestrator_agent import OrchestratorAgent
from utils.logger import logger

app = BedrockAgentCoreApp()

log = app.logger

orchestrator = OrchestratorAgent()


@tool
def inventory_orchestrator(query: str) -> str:
    """
    Routes inventory system queries
    to the correct specialized agent.
    """
    print("Executing inventory_orchestrator tool...")

    return str(
        orchestrator.route_query(query)
    )


tools = [inventory_orchestrator]


_agent = None


def get_or_create_agent():

    global _agent

    if _agent is None:

        _agent = Agent(
            model="openai.gpt-oss-20b-1:0",

            system_prompt="""
You are an Inventory AI Assistant.

You help users with:
- inventory management
- stock checks
- procurement decisions
- restocking
- product information

Use tools whenever necessary.
""",

            tools=tools
        )

    return _agent


@app.entrypoint
async def invoke(payload, context):

    logger.info("Invoking Orchestrator Agent...")

    agent = get_or_create_agent()

    user_prompt = payload.get("prompt", "")

    stream = agent.stream_async(user_prompt)

    async for event in stream:

        if "data" in event and isinstance(event["data"], str):

            yield event["data"]


if __name__ == "__main__":

    app.run()

# from strands import Agent, tool
# from bedrock_agentcore.runtime import BedrockAgentCoreApp

# from agents.router_agent import RouterAgent

# app = BedrockAgentCoreApp()

# log = app.logger

# router = RouterAgent()


# @tool
# def route_inventory_query(query: str) -> str:
#     """
#     Routes inventory-related queries
#     to the appropriate agent.
#     """

#     return str(router.route_query(query))


# tools = [route_inventory_query]


# _agent = None


# def get_or_create_agent():

#     global _agent

#     if _agent is None:

#         _agent = Agent(
#             model="openai.gpt-oss-20b-1:0",

#             system_prompt="""
#             You are an Inventory AI Assistant.

#             Help users with:
#             - inventory lookup
#             - stock checks
#             - procurement decisions
#             - low stock alerts
#             - product listings

#             Use tools whenever needed.
#             """,

#             tools=tools
#         )

#     return _agent


# @app.entrypoint
# async def invoke(payload, context):

#     log.info("Invoking Inventory Agent...")

#     agent = get_or_create_agent()

#     user_prompt = payload.get("prompt", "")

#     stream = agent.stream_async(user_prompt)

#     async for event in stream:

#         if "data" in event and isinstance(event["data"], str):

#             yield event["data"]


# if __name__ == "__main__":
#     app.run()


# from agents.router_agent import RouterAgent

# router = RouterAgent()

# print("\n=== Inventory AI System ===")

# while True:

#     query = input("\nEnter Query: ")

#     if query.lower() == "exit":
#         break

#     response = router.route_query(query)

#     print("\nResponse:")
#     print(response)


# from pydantic import BaseModel

# from fastapi import FastAPI
# from agents.router_agent import RouterAgent

# class ChatRequest(BaseModel):
#     message: str
    
# app = FastAPI()

# router = RouterAgent()

# @app.get("/")
# def home():
#     return {"message": "Inventory AI Running"}

# @app.post("/query")
# def query_inventory(q: str):
#     return {
#         "response": router.route_query(q)
#     }

# @app.post("/chat")
# def chat(request: ChatRequest):

#     response = router.route_query(request.message)

#     return {
#         "response": response
#     }


# @app.post("/invoke")
# def invoke(request: ChatRequest):

#     response = router.route_query(request.message)

#     return {
#         "response": response
#     }


# @app.post("/agent")
# def agent(request: ChatRequest):

#     response = router.route_query(request.message)

#     return {
#         "response": response
#     }