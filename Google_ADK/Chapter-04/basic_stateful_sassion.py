import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answer_agent import agent

load_dotenv()

session_service_stateful = InMemorySessionService()

initial_state = {
    "users_name": "Adnan Abdullah Sadi",
    "users_preference": """
        I like to play FC25
        My favourite color is yellow,
        I prefer coffe
        I like to watch action comedy movie
        I also want to be a Machine Learning Engineer
    """

}


# Create new Session
app_name = "Adnan's Bot"
user_id = "Adnan_abdullah"
session_id = str(uuid.uuid4())
stateful_session = session_service_stateful.create_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id,
    state=initial_state
)


print("CREATED NEW SESSION:")
print(f"\tsession_id: {session_id}")

runner = Runner(
    agent=agent.root_agent,
    app_name=app_name,
    session_service=session_service_stateful
)

new_message = types.Content(
    role="user",
    parts=[types.Part(text="What is Adnan's Favourite Color?")]
)

for event in runner.run(
    user_id=user_id,
    session_id=session_id,
    new_message=new_message
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(event.content.parts[0].text)


"""This part is completely unrelenting to the code"""
print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id
)

# Log final session state
print("==== Final Session State ====")
for key, value in session.state.items():
    print(f"{key}: {value}")