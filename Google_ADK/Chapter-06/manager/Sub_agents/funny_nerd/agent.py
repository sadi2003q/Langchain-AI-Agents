from dotenv import load_dotenv
from google.adk.tools.tool_context import ToolContext
from google.adk.agents import Agent

load_dotenv()


def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    """Pass the topic to the LLM to generate the joke."""
    print(f"--- Tool: get_nerd_joke called for topic: {topic} ---")

    valid_topics = [
        "python", "javascript", "java",
        "programming", "math", "physics",
        "chemistry", "biology"
    ]

    if topic.lower() not in valid_topics:
        return {
            "status": "error",
            "message": f"'{topic}' is not a supported topic.",
            "supported_topics": valid_topics
        }

    tool_context.state["last_joke_topic"] = topic
    return {"status": "ok", "topic": topic}


funny_nerd = Agent(
    name="funny_nerd",
    model="gemini-2.0-flash-001",
    description="An agent that tells nerdy jokes about various topics.",
    instruction="""
    You are a funny nerd agent that tells nerdy jokes about various topics.
        
        When asked to tell a joke:
        1. Call the get_nerd_joke tool to validate and retrieve the topic
        2. Then generate a joke yourself using your own knowledge about that topic
        3. Format the response to include both the joke and a brief explanation if needed
        
        If the topic is invalid, show an error message listing valid topics.
        
        Example response format:
        "Here's a nerdy joke about <TOPIC>:
        <JOKE>
        
        Explanation: {brief explanation if needed}"
        
        If the user asks about anything else, delegate the task to the manager agent.
    """
)