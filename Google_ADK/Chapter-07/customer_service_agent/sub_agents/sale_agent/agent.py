from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from dotenv import load_dotenv

load_dotenv()


def purchase_course(tool_context: ToolContext) -> dict:
    course_id = "ai_marketing_platform",
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    current_purchased_course = tool_context.state.get('purchased_courses')

    course_ids = [
        course['id'] for course in current_purchased_course if isinstance(course, dict)
    ]

    if course_id in course_ids:
        return {
            "status": "Error",
            "message": "You already own this course!"
        }

    new_purchased_course = []

    for course in current_purchased_course:
        if isinstance(course, dict) and "id" in course.keys():
            new_purchased_course.append(course)

    new_purchased_course.append({
        "id": course_id,
        "purchased_date": current_time
    })

    tool_context.state["purchased_courses"] = new_purchased_course

    current_interaction_history = tool_context.state["interaction_history"]
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "purchased_course",
        "course_id": course_id,
        "timestamp": current_time
    })

    tool_context.state["interaction_history"] = new_interaction_history
    return {
        "status": "success",
        "message": "Successfully purchased the AI Marketing Platform course!",
        "course_id": course_id,
        "timestamp": current_time,
    }


# with open("course_details.txt", "r") as file:
#     course_details_file = file.read()

course_details_file= """
Course Details:
    - Name: Fullstack AI Marketing Platform
    - Price: $149
    - Value Proposition: Learn to build AI-powered marketing automation apps
    - Includes: 6 weeks of group support with weekly coaching calls

"""


sale_agent = Agent(
    name="sale_agent",
    model="gemini-2.0-flash",
    description="Sales agent for the AI Marketing Platform course",
    instruction=f"""
    You are a sales agent for the AI Developer Accelerator community, specifically handling sales
    for the Fullstack AI Marketing Platform course.

    <user_info>
    Name: {{user_name}}
    </user_info>

    <purchase_info>
    Purchased Courses: {{purchased_courses}}
    </purchase_info>

    <interaction_history>
    {{interaction_history}}
    </interaction_history>

    {course_details_file}

    When interacting with users:
    1. Check if they already own the course (check purchased_courses above)
       - Course information is stored as objects with "id" and "purchase_date" properties
       - The course id is "ai_marketing_platform"
    2. If they own it:
       - Remind them they have access
       - Ask if they need help with any specific part
       - Direct them to course support for content questions

    3. If they don't own it:
       - Explain the course value proposition
       - Mention the price ($149)
       - If they want to purchase:
           - Use the purchase_course tool
           - Confirm the purchase
           - Ask if they'd like to start learning right away

    4. After any interaction:
       - The state will automatically track the interaction
       - Be ready to hand off to course support after purchase

    Remember:
    - Be helpful but not pushy
    - Focus on the value and practical skills they'll gain
    - Emphasize the hands-on nature of building a real AI application
    """,
    tools=[purchase_course]
)
