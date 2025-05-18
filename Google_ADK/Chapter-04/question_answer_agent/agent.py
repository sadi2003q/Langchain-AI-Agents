from google.adk.agents import Agent
from dotenv import load_dotenv


load_dotenv()


root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='question_answer_agent',
    description='Question Answering Agent',
    instruction="""
    you are a helpful agent who answer question about the users preference
    here is some information about the user:
    
    - name: {users_name}
    - preference: {users_preference}
    
    """,
)
