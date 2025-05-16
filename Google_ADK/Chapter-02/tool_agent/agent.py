from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search


def get_current_time() -> dict:
    """
    Get the current time in the format 'hh:mm:ss'
    :return: time in format 'hh:mm:ss'
    """
    return {
        'current_Time': datetime.now().strftime('%H:%M:%S')
    }


root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get_current_time
    """,
    # tools=[google_search]
    tools=[get_current_time]
)
