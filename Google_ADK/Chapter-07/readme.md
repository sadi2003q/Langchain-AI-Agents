# 🤝 Customer Service Multi-Agent System

Welcome to the **Customer Service Multi-Agent System**! This project is a Python-based application designed to provide customer support for the AI Developer Accelerator community. It uses a hierarchical agent system where a central customer service agent delegates tasks to specialized sub-agents handling course support, sales, orders, and policy inquiries. The system is built with extensibility in mind, leveraging the `google.adk` framework.

---

## 🚀 Project Overview

The project creates a customer service ecosystem for users of the AI Developer Accelerator community, specifically for the "Fullstack AI Marketing Platform" course. Key features include:

- **Customer Service Agent**: The main agent that routes user queries to specialized sub-agents.
- **Course Support Agent**: Assists users with course content, ensuring they own the course.
- **Sales Agent**: Handles course purchases and provides course details.
- **Order Agent**: Manages purchase history and processes refunds.
- **Policy Agent**: Answers questions about community guidelines and policies.

The system maintains user state (e.g., purchase history, interaction history) using an in-memory session service, ensuring personalized responses.

---

## 📂 Project Structure

The project is organized under the `Chapter-07` directory with the following structure:

```
Chapter-07/
├── customer_service_agent/          # Main customer service agent module
│   └── agent.py                    # Defines the customer service agent for routing queries
├── sub_agents/                     # Specialized sub-agents for specific tasks
│   ├── course_suppoer_agent/       # Course Support Agent module (note: typo in folder name)
│   │   ├── agent.py                # Implements the agent for course content support
│   │   └── course_instruction.txt  # Contains course section details
│   ├── order_agent/                # Order Agent module
│   │   └── agent.py                # Implements the agent for purchase history and refunds
│   ├── policy_agent/               # Policy Agent module
│   │   ├── agent.py                # Implements the agent for policy inquiries
│   │   └── policy.txt              # Contains community guidelines and policies
│   └── sale_agent/                 # Sales Agent module
│       └── agent.py                # Implements the agent for course sales
├── .env                            # Environment variables (e.g., API keys)
├── __init__.py                     # Initializes the project root
├── main.py                         # Entry point for the application
└── utils.py                        # Utility functions for session management and response formatting
```

**Note**: The folder `course_suppoer_agent` appears to have a typo and should likely be `course_support_agent`.

---

## 🛠️ Code Overview with Examples

### 1. Customer Service Agent
The `customer_service_agent` acts as the main entry point, routing user queries to the appropriate sub-agent.

**Example Code** (from `customer_service_agent/agent.py`):
```python
customer_service_agent = Agent(
    name="customer_service",
    model="gemini-2.0-flash",
    description="Customer service agent for AI Developer Accelerator community",
    instruction="""
    You are the primary customer service agent for the AI Developer Accelerator community.
    Your role is to help users with their questions and direct them to the appropriate specialized agent.
    ...
    """,
    sub_agents=[policy_agent, sale_agent, course_support_agent, order_agent],
    tools=[],
)
```

**Usage Example**:
If a user asks, "Can I get a refund for the AI Marketing Platform course?" the agent routes the query to the `order_agent`, which might respond:
```
I've processed your refund for the Fullstack AI Marketing Platform course.
Your $149 will be returned to your original payment method within 3-5 business days.
The course has been removed from your account.
```

---

### 2. Course Support Agent
The `course_support_agent` helps users with course content, ensuring they own the course.

**Example Code** (from `sub_agents/course_suppoer_agent/agent.py`):
```python
course_support_agent = Agent(
    name="course_support_agent",
    model="gemini-2.0-flash",
    description="Course support agent for the AI Marketing Platform course",
    instruction="""
    You are the course support agent for the Fullstack AI Marketing Platform course.
    Your role is to help users with questions about course content and sections.
    ...
    """,
    tools=[],
)
```

**Usage Example**:
If a user who owns the course asks, "How do I set up NextJS?" the agent might respond:
```
You can find guidance on setting up NextJS in Section 7: NextJS Crash Course and Section 8: Stub Out NextJS App. These sections cover the fundamentals, routing, and initial app setup. I recommend starting with the hands-on exercises in Section 8 to create your app structure.
```

---

### 3. Sales Agent
The `sale_agent` handles course purchases and provides course details.

**Example Code** (from `sub_agents/sale_agent/agent.py`):
```python
def purchase_course(tool_context: ToolContext) -> dict:
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    current_purchased_course = tool_context.state.get('purchased_courses')
    ...
    return {
        "status": "success",
        "message": "Successfully purchased the AI Marketing Platform course!",
        "course_id": course_id,
        "timestamp": current_time,
    }
```

**Usage Example**:
If a user asks to buy the course, the agent might respond:
```
Successfully purchased the AI Marketing Platform course! Would you like to start learning right away?
```

---

### 4. Order Agent
The `order_agent` manages purchase history and processes refunds.

**Example Code** (from `sub_agents/order_agent/agent.py`):
```python
def refund_course(tool_context: ToolContext) -> dict:
    course_id = "ai_marketing_platform"
    current_time = get_current_time()
    current_purchased_courses = tool_context.state.get("purchased_course", [])
    ...
    return {
        "state": 'success',
        "message": "Successfully refunded the AI Marketing Platform course! Your $149 will be returned to your original payment method within 3-5 business days.",
        'course_id': course_id,
        'timestamp': current_time
    }
```

**Usage Example**:
If a user requests a refund within 30 days, the agent might respond:
```
I've processed your refund for the Fullstack AI Marketing Platform course.
Your $149 will be returned to your original payment method within 3-5 business days.
The course has been removed from your account.
```

---

### 5. Policy Agent
The `policy_agent` answers questions about community guidelines and policies.

**Example Code** (from `sub_agents/policy_agent/agent.py`):
```python
base_instruction = f"""
You are the policy agent for the AI Developer Accelerator community. Your role is to help users understand our community guidelines and policies.
...
{policy_file}
"""
```

**Usage Example**:
If a user asks about the refund policy, the agent might respond:
```
Our refund policy offers a 30-day money-back guarantee. You can request a full refund within 30 days of purchase, no questions asked. If you complete the course and aren't satisfied, you're still eligible for a refund within this period.
```

---

## 🏃 How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Install required packages:
  ```bash
  pip install python-dotenv google-adk
  ```
- Set up a `.env` file in the project root with necessary API keys (e.g., for `google.adk`).

### Steps to Run
1. Clone the repository or navigate to the `Chapter-07` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If a `requirements.txt` is not present, use the command under Prerequisites.)
3. Ensure the `.env` file is configured with required environment variables.
4. Run the main application:
   ```bash
   python main.py
   ```
5. Follow the interactive prompts to chat with the customer service agent. Type `exit` or `quit` to end the conversation.

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

**Built with ❤️ by the sadi_AI Community**
