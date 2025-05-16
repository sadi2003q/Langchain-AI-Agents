# Tools in Google ADK

Google's Agent Development Kit (ADK) provides a flexible framework for building and deploying AI agents. One of its core components is its **tools system**, which enables agents to interact with the environment, APIs, or other agents. These tools can be classified into three main categories:

---

## 1. Function Tool

Function tools are callable functions or methods that an agent can use to perform specific tasks. These are defined by the developer and can be integrated into the agent's reasoning and execution pipeline.

### - Functions/Methods  
These are Python or other language-defined functions wrapped as tools. They follow a specific schema, typically with:
- Name
- Description
- Parameters (with types and constraints)

**Example:**
```python
def get_weather(city: str) -> str:
    # Fetches weather info
    ...