import logging
from typing import Dict, Any

import requests
from strands.models import BedrockModel
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent, tool

# -----------------------------
# Logger Configuration
# -----------------------------
logger = logging.getLogger("ifsc-agent")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
)
logger.addHandler(handler)

# -----------------------------
# Config
# -----------------------------
IFSC_API_BASE = "https://ifsc.razorpay.com"


def _normalize_ifsc(ifsc: str) -> str:
    """Basic cleaning/normalization of IFSC code."""
    if not ifsc:
        return ""
    return ifsc.strip().upper()


def _is_valid_ifsc(ifsc: str) -> bool:
    """
    Very simple validation:
    - length 11
    - alphanumeric
    """
    return len(ifsc) == 11 and ifsc.isalnum()


# -----------------------------
# Tool
# -----------------------------
@tool
def get_ifsc_info(ifsc_code: str) -> Dict[str, Any]:
    """
    Look up bank & branch information for a given IFSC code.

    Arguments:
        ifsc_code: Indian IFSC code, e.g. 'HDFC0001234'.

    Returns:
        {
          "success": bool,
          "message": str,
          "ifsc": str | None,
          "bank": str | None,
          "branch": str | None,
          "address": str | None,
          "city": str | None,
          "state": str | None,
          "contact": str | None,
          "micr": str | None,
          "upi": bool | None,
          "neft": bool | None,
          "rtgs": bool | None,
          "imps": bool | None,
          "raw": dict | None       # full raw payload from API
        }
    """
    logger.info(f"🛠 get_ifsc_info invoked for IFSC={ifsc_code!r}")

    ifsc = _normalize_ifsc(ifsc_code)
    if not _is_valid_ifsc(ifsc):
        logger.warning(f"Invalid IFSC format: {ifsc!r}")
        return {
            "success": False,
            "message": "Invalid IFSC format. It should be 11 alphanumeric characters.",
            "ifsc": ifsc,
            "bank": None,
            "branch": None,
            "address": None,
            "city": None,
            "state": None,
            "contact": None,
            "micr": None,
            "upi": None,
            "neft": None,
            "rtgs": None,
            "imps": None,
            "raw": None,
        }

    url = f"{IFSC_API_BASE}/{ifsc}"
    logger.info(f"Calling IFSC API: {url}")

    try:
        resp = requests.get(url, timeout=5)
    except Exception as e:
        logger.error(f"Error calling IFSC API: {e}")
        return {
            "success": False,
            "message": "Error calling IFSC API. Please try again later.",
            "ifsc": ifsc,
            "bank": None,
            "branch": None,
            "address": None,
            "city": None,
            "state": None,
            "contact": None,
            "micr": None,
            "upi": None,
            "neft": None,
            "rtgs": None,
            "imps": None,
            "raw": None,
        }

    if resp.status_code != 200:
        logger.warning(f"IFSC API responded with status={resp.status_code}")
        return {
            "success": False,
            "message": f"IFSC not found or API error (status {resp.status_code}).",
            "ifsc": ifsc,
            "bank": None,
            "branch": None,
            "address": None,
            "city": None,
            "state": None,
            "contact": None,
            "micr": None,
            "upi": None,
            "neft": None,
            "rtgs": None,
            "imps": None,
            "raw": None,
        }

    data = resp.json()

    # Razorpay IFSC API returns "Not Found" as plain text sometimes
    if isinstance(data, str):
        logger.warning(f"IFSC API returned non-JSON body: {data!r}")
        return {
            "success": False,
            "message": "IFSC not found.",
            "ifsc": ifsc,
            "bank": None,
            "branch": None,
            "address": None,
            "city": None,
            "state": None,
            "contact": None,
            "micr": None,
            "upi": None,
            "neft": None,
            "rtgs": None,
            "imps": None,
            "raw": None,
        }

    result = {
        "success": True,
        "message": "IFSC details fetched successfully.",
        "ifsc": data.get("IFSC"),
        "bank": data.get("BANK"),
        "branch": data.get("BRANCH"),
        "address": data.get("ADDRESS"),
        "city": data.get("CITY"),
        "state": data.get("STATE"),
        "contact": data.get("CONTACT"),
        "micr": data.get("MICR"),
        "upi": data.get("UPI"),
        "neft": data.get("NEFT"),
        "rtgs": data.get("RTGS"),
        "imps": data.get("IMPS"),
        "raw": data,
    }

    logger.info(
        f"✅ IFSC lookup success: {result['bank']} - {result['branch']} ({result['ifsc']})"
    )
    return result


# -----------------------------
# Agent / Model
# -----------------------------
SYSTEM_PROMPT = """
You are an Indian Bank IFSC & Branch Lookup Assistant.

Capabilities:
- You can look up bank and branch details for an IFSC code using the `get_ifsc_info` tool.
- You must ALWAYS call the tool when the user provides, or asks about, a specific IFSC code.
- Never invent bank details. Use ONLY the values returned by the tool.
- If `success` is False, clearly explain that the IFSC seems invalid or not found.
- When explaining results, clearly mention:
    - Bank name
    - Branch name
    - City and State
    - Address
    - Supported payment methods (UPI / NEFT / RTGS / IMPS) if available.
- If the user asks general questions about IFSC (not a specific code),
  you can answer from your own knowledge without calling the tool.
- Do not return any thinking like tags, it should be human mimicing answer.
"""

app = BedrockAgentCoreApp()

bedrock_model = BedrockModel(
    model_id="openai.gpt-oss-safeguard-120b",
    temperature=0.1,
    region_name="us-east-1",
    max_tokens=2048,
)

agent = Agent(
    model=bedrock_model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_ifsc_info],
)


@app.entrypoint
def invoke(payload: Dict[str, Any]):
    """
    Expected payload example:
        {
          "prompt": "Give me details for IFSC HDFC0001234"
        }
    """
    user_message = payload.get("prompt", "I want to check an IFSC code.")
    result = agent(user_message)
    return {"result": result.message}


if __name__ == "__main__":
    app.run()
