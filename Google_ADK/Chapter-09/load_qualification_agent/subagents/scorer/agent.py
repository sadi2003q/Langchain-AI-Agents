from google.adk.agents import Agent
from dotenv import load_dotenv

load_dotenv()

lead_score_agent = Agent (
    name="scorer",
    model="gemini-2.0-flash",
    description="Scores Qualified lean on a scale of 1-10",
    instruction="""
    You are a Lead Scoring AI.
    
    Analyze the lead information and assign a qualification score from 1-10 based on:
    - Expressed need (urgency/clarity of problem)
    - Decision-making authority
    - Budget indicators
    - Timeline indicators
    
    Output ONLY a numeric score and ONE sentence justification.
    
    Example output: '8: Decision maker with clear budget and immediate need'
    Example output: '3: Vague interest with no timeline or budget mentioned'
    """,
    output_key="lead_score"
)