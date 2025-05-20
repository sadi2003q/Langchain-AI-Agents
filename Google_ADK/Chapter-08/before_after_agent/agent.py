from datetime import datetime
from google.adk.agents import Agent
from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.genai import types


def before_agent_call(callback_context: CallbackContext) -> Optional[types.Content]:
    state = callback_context.state
    timestamp = datetime.now()

    if "agent_name" not in state:
        state['agent_name'] = "SimpleChatbot"

    state["request_counter"] = state.get("request_counter", 0) + 1
    state["request_start_time"] = timestamp
    return None


def after_agent_call(callback_context:CallbackContext)->Optional[types.Content]:
    state = callback_context.state
    timestamp = datetime.now()
    duration = -1
    if "request_start_time" in state:
        duration = (timestamp - state['request_start_time']).total_seconds()
    if duration is not -1:
        print(f"[AFTER CALLBACK] Processing took {duration:.2f} seconds")
    return None


root_agent = Agent(
    name="before_after_agent",
    model="gemini-2.0-flash",
    description="A basic agent that demonstrates before and after agent callbacks",
    instruction="""
        You are a friendly greeting agent. Your name is {agent_name}.

        Your job is to:
        - Greet users politely
        - Respond to basic questions
        - Keep your responses friendly and concise
        """,
    before_agent_callback=before_agent_call,
    after_agent_callback=after_agent_call
)
