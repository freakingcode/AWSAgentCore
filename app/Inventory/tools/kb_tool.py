import boto3
from strands import tool

bedrock_agent_runtime = boto3.client(
    "bedrock-agent-runtime",
    region_name="us-east-1"
)

KNOWLEDGE_BASE_ID = "YOUR_KB_ID"


@tool
def search_inventory_knowledge(query: str) -> str:
    """
    Search inventory knowledge base.
    """

    response = bedrock_agent_runtime.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={
            "text": query
        }
    )

    results = response.get("retrievalResults", [])

    if not results:
        return "No relevant information found."

    context = []

    for item in results[:5]:
        text = item["content"]["text"]
        context.append(text)

    return "\n\n".join(context)