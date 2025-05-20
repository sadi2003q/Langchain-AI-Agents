from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from dotenv import load_dotenv

load_dotenv()

def get_current_time() -> dict:
    """Get the current time in the format YYYY-MM-DD HH:MM:SS
    :return: "current_time": {Value}
    """

    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def refund_course(tool_context: ToolContext) -> dict:
    """
    Simulates refunding the AI market platform course.
    Update state by removing the course from purchased_course
    :param tool_context:
    :return:  A dictionary with refund status, message, course ID, and timestamp
    """
    course_id = "ai_marketing_platform"
    current_time = get_current_time()

    current_purchased_courses = tool_context.state.get("purchased_course", [])
    course_ids = [
        course['id'] for course in current_purchased_courses if isinstance(course, dict)
    ]

    if course_id not in course_ids:
        return {
            'status': 'error',
            'message': 'You dont own this course so it cannot be refunded.'
        }
    new_purchased_courses = []
    for course in current_purchased_courses:
        if not course or not isinstance(course, dict):
            continue
        if course.get('id') == course_id:
            continue
        new_purchased_courses.append(course)

    tool_context.state["purchased_courses"] = new_purchased_courses

    current_interaction_history = tool_context.state.get("interaction_history", [])

    new_interation_history = current_interaction_history.copy()
    new_interation_history.append(
        {
            "action": "refund_course",
            "course_id": course_id,
            'timestamp': current_time
        }
    )

    tool_context.state["interaction_history"] = new_interation_history

    return {
        "state": 'success',
        "message": """
        Successfully refunded the AI Marketing Platform course! 
         Your $149 will be returned to your original payment method within 3-5 business days.
        """,
        'course_id': course_id,
        'timestamp': current_time

    }


order_agent = Agent(
    name="order_agent",
    model='gemini-2.0-flash',
    description="Order agent for viewing purchased history and processing refunds",
    instruction="""
    You are the order agent for the AI Developer Accelerator community.
    Your role is to help users view their purchase history, course access, and process refunds.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    When users ask about their purchases:
    1. Check their course list from the purchase info above
       - Course information is stored as objects with "id" and "purchase_date" properties
    2. Format the response clearly showing:
       - Which courses they own
       - When they were purchased (from the course.purchase_date property)

    When users request a refund:
    1. Verify they own the course they want to refund ("ai_marketing_platform")
    2. If they own it:
       - Use the refund_course tool to process the refund
       - Confirm the refund was successful
       - Remind them the money will be returned to their original payment method
       - If it's been more than 30 days, inform them that they are not eligible for a refund
    3. If they don't own it:
       - Inform them they don't own the course, so no refund is needed

    Course Information:
    - ai_marketing_platform: "Fullstack AI Marketing Platform" ($149)

    Example Response for Purchase History:
    "Here are your purchased courses:
    1. Fullstack AI Marketing Platform
       - Purchased on: 2024-04-21 10:30:00
       - Full lifetime access"

    Example Response for Refund:
    "I've processed your refund for the Fullstack AI Marketing Platform course.
    Your $149 will be returned to your original payment method within 3-5 business days.
    The course has been removed from your account."

    If they haven't purchased any courses:
    - Let them know they don't have any courses yet
    - Suggest talking to the sales agent about the AI Marketing Platform course

    Remember:
    - Be clear and professional
    - Mention our 30-day money-back guarantee if relevant
    - Direct course questions to course support
    - Direct purchase inquiries to sales
    """,
    tools=[refund_course, get_current_time]
)
