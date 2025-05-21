from google.adk.agents import SequentialAgent
from .subagents.recommender.agent import action_recommendation_agent
from .subagents.validator.agent import lead_validator_agent
from .subagents.scorer.agent import lead_score_agent


root_agent = SequentialAgent(
    name="load_qualification_agent",
    sub_agents=[lead_validator_agent, lead_score_agent, action_recommendation_agent],
    description="A pipeline that validates, scores and recommends actions for sales leads"

)
