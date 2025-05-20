# 🛠️ Before/After Callbacks Demo

Welcome to the **Before/After Callbacks Demo**! This project demonstrates the use of callbacks in the `google.adk` framework to enhance agent functionality. It showcases three types of callbacks—agent, model, and tool—through practical examples, such as tracking request times, filtering content, and processing flight price data.

---

## 🚀 Project Overview

This project explores the power of callbacks in the `google.adk` framework, which allows developers to inject custom logic before and after key operations in an agent's lifecycle. The project is divided into three modules:

- **Before/After Agent Callback**: Tracks request counts and processing times for a simple chatbot.
- **Before/After Model Callback**: Filters inappropriate language and modifies model responses for better tone.
- **Before/After Tool Callback**: Sanitizes inputs and enhances outputs for a flight price checker tool.

Each module highlights a different use case for callbacks, demonstrating their flexibility in real-world applications.

---

## 📂 Project Structure

The project is organized under the `Chapter-08` directory with the following structure:

```
Chapter-08/
├── before_after_agent/         # Agent callback demo
│   ├── .env                    # Environment variables (e.g., API keys)
│   ├── __init__.py             # Initializes the module
│   └── agent.py                # Implements the agent with before/after agent callbacks
├── before_after_model/         # Model callback demo
│   ├── .env                    # Environment variables
│   ├── __init__.py             # Initializes the module
│   └── agent.py                # Implements the agent with before/after model callbacks
├── before_after_tool/          # Tool callback demo
│   ├── .env                    # Environment variables
│   ├── __init__.py             # Initializes the module
│   └── agent.py                # Implements the agent with before/after tool callbacks
```

---

## 🤔 What Are Before/After Callbacks?

Callbacks in the `google.adk` framework allow you to execute custom logic at specific points in an agent's lifecycle. They are powerful tools for logging, validation, and response modification. The project demonstrates three types of callbacks:

### 1. Agent Callbacks
- **Before Agent Callback**: Runs before the agent processes a user request. Useful for initializing state or logging.
- **After Agent Callback**: Runs after the agent finishes processing. Ideal for logging metrics like processing time.
- **Use Case**: In `before_after_agent`, the callbacks track the number of requests and calculate processing duration.

### 2. Model Callbacks
- **Before Model Callback**: Executes before the language model processes the input. Useful for input validation or filtering.
- **After Model Callback**: Executes after the model generates a response. Allows for response modification or logging.
- **Use Case**: In `before_after_model`, the callbacks filter inappropriate language and replace negative words (e.g., "problem" with "challenge").

### 3. Tool Callbacks
- **Before Tool Callback**: Runs before a tool is called. Useful for input sanitization or validation.
- **After Tool Callback**: Runs after the tool returns a response. Allows for output enhancement or formatting.
- **Use Case**: In `before_after_tool`, the callbacks fix city name typos and append additional information to flight prices.

---

## 🛠️ Code Overview with Examples

### 1. Before/After Agent Callback
The `before_after_agent` module demonstrates agent-level callbacks by tracking request counts and processing times.

**Example Code** (from `before_after_agent/agent.py`):
```python
def before_agent_call(callback_context: CallbackContext) -> Optional[types.Content]:
    state = callback_context.state
    timestamp = datetime.now()
    if "agent_name" not in state:
        state['agent_name'] = "SimpleChatbot"
    state["request_counter"] = state.get("request_counter", 0) + 1
    state["request_start_time"] = timestamp
    return None

def after_agent_call(callback_context: CallbackContext) -> Optional[types.Content]:
    state = callback_context.state
    timestamp = datetime.now()
    duration = -1
    if "request_start_time" in state:
        duration = (timestamp - state['request_start_time']).total_seconds()
    if duration is not -1:
        print(f"[AFTER CALLBACK] Processing took {duration:.2f} seconds")
    return None
```

**Explanation**:
- `before_agent_call`: Increments a request counter and stores the start time in the state.
- `after_agent_call`: Calculates the processing duration by comparing the start and end times, then logs it.

**Usage Example**:
If a user sends a message, the agent might log:
```
[AFTER CALLBACK] Processing took 0.85 seconds
```

---

### 2. Before/After Model Callback
The `before_after_model` module uses model-level callbacks to filter inappropriate language and modify responses.

**Example Code** (from `before_after_model/agent.py`):
```python
def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    state = callback_context.state
    last_user_message = ""
    for content in reversed(llm_request.contents):
        if content.role == "user" and content.parts and hasattr(content.parts[0], "text"):
            last_user_message = content.parts[0].text
            break
    if last_user_message and "sucks" in last_user_message.lower():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="I cannot respond to messages containing inappropriate language")]
            )
        )
    state["model_start_time"] = datetime.now()
    return None

def after_model_callback(llm_response: LLMResponse) -> Optional[LlmResponse]:
    response_text = ""
    for part in llm_response.content.parts:
        if hasattr(part, "text") and part.text:
            response_text += part.text
    replacements = {"problem": "challenge", "difficult": "complex"}
    modified_text = response_text
    modified = False
    for original, replacement in replacements.items():
        if original in modified_text.lower():
            modified_text = modified_text.replace(original, replacement)
            modified = True
    if modified:
        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        for i, part in enumerate(modified_parts):
            if hasattr(part, "text"):
                modified_parts[i].text = modified_text
        return LlmResponse(content=types.Content(role="model", parts=modified_parts))
    return None
```

**Explanation**:
- `before_model_callback`: Checks for inappropriate words (e.g., "sucks") and blocks the response if found.
- `after_model_callback`: Replaces negative words like "problem" with "challenge" to improve tone.

**Usage Example**:
If a user says, "This problem is difficult," the agent might respond:
```
This challenge is complex.
```

---

### 3. Before/After Tool Callback
The `before_after_tool` module demonstrates tool-level callbacks by sanitizing inputs and enhancing outputs for a flight price checker.

**Example Code** (from `before_after_tool/agent.py`):
```python
def before_tool_callback(tool: BaseTool, args: Dict[str, Any], context: ToolContext) -> Optional[Dict]:
    origin = args.get("origin", "").strip().lower()
    destination = args.get("destination", "").strip().lower()
    typo_fixes = {"nyc": "new york", "la": "los angeles", "del": "delhi"}
    if origin in typo_fixes:
        args["origin"] = typo_fixes[origin]
    if destination in typo_fixes:
        args["destination"] = typo_fixes[destination]
    if destination in ["pyongyang", "mosul"]:
        return {"result": f"Flights to {destination.title()} are currently restricted for safety reasons."}
    return None

def after_tool_callback(tool: BaseTool, args: Dict[str, Any], context: ToolContext, response: Dict) -> Optional[Dict]:
    result = response.get("result", "")
    if "$" in result:
        modified = copy.deepcopy(response)
        modified["result"] = f"✈️ Estimated price: {result} (including taxes)"
        return modified
    return None
```

**Explanation**:
- `before_tool_callback`: Fixes city name typos (e.g., "nyc" to "new york") and blocks restricted destinations.
- `after_tool_callback`: Enhances the flight price output by adding a prefix and tax information.

**Usage Example**:
If a user asks for a flight price from "nyc" to "paris", the agent might respond:
```
✈️ Estimated price: $550 (including taxes)
```

---

## 🏃 How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Install required packages:
  ```bash
  pip install python-dotenv google-adk litellm
  ```
- Set up a `.env` file in each module directory with necessary API keys (e.g., for `google.adk`).

### Steps to Run
1. Clone the repository or navigate to the `Chapter-08` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If a `requirements.txt` is not present, use the command under Prerequisites.)
3. Navigate to the desired module (e.g., `before_after_agent`):
   ```bash
   cd before_after_agent
   ```
4. Ensure the `.env` file is configured with required environment variables.
5. Run the agent:
   ```bash
   python agent.py
   ```
6. Repeat for other modules (`before_after_model`, `before_after_tool`) as needed.

**Note**: This project is a demo and does not include a `main.py` for interactive execution. You can test each agent by integrating it into a runner or client application.

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

**Built with ❤️ by the Sadi_AI Community**
