from google.adk.agents import Agent
from pydantic import BaseModel, Field


class EmailAgent_outputSchema(BaseModel):
    subject: str = Field(..., description="The subject line of the email. should be concise and to the point")
    body: str = Field(..., description="""
                        The content of the email. Should be well formatted with proper greeting 
                        paragraph and end with conclusion. 
                    """)


root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='email_agent',
    description='Generate professional emails with structured subject and body',
    instruction="""
            You are an Email Generation Assistant.
        Your task is to generate a professional email based on the user's request.
        
        GUIDELINES:
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
          * Professional greeting
          * Clear and concise main content
          * Appropriate closing
          * Your name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete
        
        IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting"
        }
        
        DO NOT include any explanations or additional text outside the JSON response.
    """,
    output_schema=EmailAgent_outputSchema,
    output_key="email"
)


