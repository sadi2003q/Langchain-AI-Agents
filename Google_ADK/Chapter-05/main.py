from dotenv import load_dotenv
import asyncio
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent

load_dotenv()


async def call_agent_async(runner, user_id:str, session_id: str, query: str):
    """Call the agent asynchronously and return the final response from agent"""
    content = types.Content(role="user", parts= [types.Part(text=query)])

    async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(event.content.parts[0].text)


async def main_async():
    app_name = "Adnan's App"
    user_id = "ai_with_adnan"

    # Create Database for sessions
    session_service = DatabaseSessionService(db_url="sqlite:///./my_agent_data.db")

    # Create sessions or get sessions
    sessions = session_service.list_sessions(app_name=app_name, user_id=user_id)
    if sessions and sessions.sessions:
        session_id = sessions.sessions[0].id
    else:
        session = session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            state={
                "user_name": "I am Muslim",
                "reminders": []
            }
        )
        session_id = session.id
    runner= Runner(
        app_name=app_name,
        agent=memory_agent,
        session_service=session_service
    )

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        await call_agent_async(runner, user_id, session_id, user_input)

if __name__ == "__main__":
    asyncio.run(main_async())

# set me a reminder at 5pm about online class