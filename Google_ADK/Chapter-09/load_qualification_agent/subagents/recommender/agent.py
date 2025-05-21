from google.adk.agents import Agent
from dotenv import load_dotenv

load_dotenv()

action_recommendation_agent = Agent(
    name="recommender",
    model="gemini-2.0-flash",
    description="Recommend Next Action Based on lead Qualification",
    instruction="""
    You are an Action Recommendation AI.
    
    Based on the lead information and scoring:
    
    - For invalid leads: Suggest what additional information is needed
    - For leads scored 1-3: Suggest nurturing actions (educational content, etc.)
    - For leads scored 4-7: Suggest qualifying actions (discovery call, needs assessment)
    - For leads scored 8-10: Suggest sales actions (demo, proposal, etc.)
    
    Format your response as a complete recommendation to the sales team.
    
    Lead Score:
    {lead_score}

    Lead Validation Status:
    {validation_status}
    """,
    output_key="action_recommendation"
)