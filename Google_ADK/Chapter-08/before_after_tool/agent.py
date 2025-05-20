"""
Real-World Example: Flight Price Checker using Tool Callbacks

This shows how before and after callbacks can sanitize inputs and post-process outputs.
"""

import copy
from typing import Any, Dict, Optional

from google.adk.agents import LlmAgent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext


# --- Simulated Flight Tool ---
def check_flight_price(origin: str, destination: str) -> Dict[str, str]:
    """
    Simulates checking the price of a flight from origin to destination.
    """
    print(f"[TOOL] Checking flight price from {origin} to {destination}")

    flight_prices = {
        ("new york", "paris"): "$550",
        ("los angeles", "tokyo"): "$820",
        ("delhi", "london"): "$620",
        ("sydney", "singapore"): "$480",
    }

    key = (origin.lower(), destination.lower())
    price = flight_prices.get(key, "No flight data available.")
    print(f"[TOOL] Returning: {{'result': '{price}'}}")
    return {"result": price}


# --- Before Callback ---
def before_tool_callback(tool: BaseTool, args: Dict[str, Any], context: ToolContext) -> Optional[Dict]:
    print(f"[Callback] Before tool: {tool.name} with args: {args}")

    origin = args.get("origin", "").strip().lower()
    destination = args.get("destination", "").strip().lower()

    # Fix common typos
    typo_fixes = {"nyc": "new york", "la": "los angeles", "del": "delhi"}

    if origin in typo_fixes:
        print(f"[Callback] Fixing origin typo: {origin} → {typo_fixes[origin]}")
        args["origin"] = typo_fixes[origin]

    if destination in typo_fixes:
        print(f"[Callback] Fixing destination typo: {destination} → {typo_fixes[destination]}")
        args["destination"] = typo_fixes[destination]

    # Block travel to restricted areas
    if destination in ["pyongyang", "mosul"]:
        print("[Callback] Blocked destination.")
        return {"result": f"Flights to {destination.title()} are currently restricted for safety reasons."}

    return None


# --- After Callback ---
def after_tool_callback(tool: BaseTool, args: Dict[str, Any], context: ToolContext, response: Dict) -> Optional[Dict]:
    print(f"[Callback] After tool: {tool.name} with response: {response}")

    result = response.get("result", "")
    if "$" in result:
        modified = copy.deepcopy(response)
        modified["result"] = f"✈️ Estimated price: {result} (including taxes)"
        print(f"[Callback] Modified response: {modified}")
        return modified

    return None


# --- Agent Setup ---
flight_agent = LlmAgent(
    name="before_after_tool",
    model="gemini-2.0-pro",
    description="Agent to check flight prices using tool callbacks",
    instruction="""
    You are a helpful travel assistant.

    Your job is to check flight prices using the check_flight_price tool.
    Use exactly the cities mentioned by the user unless the callback modifies them.
    Do not generate your own flight prices.
    """,
    tools=[check_flight_price],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)