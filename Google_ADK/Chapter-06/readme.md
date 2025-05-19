# 📊 Multi-Agent System Project

Welcome to the **Multi-Agent System Project**! This project is a modular Python application that leverages a manager agent to delegate tasks to specialized sub-agents. Each sub-agent handles a specific domain, such as generating nerdy jokes, analyzing news, or fetching stock prices. The system is designed to be extensible, allowing for easy addition of new agents and tools.

---

## 🚀 Project Overview

The project implements a hierarchical agent system using the `google.adk` framework. A root manager agent oversees task delegation to sub-agents, which include:

- **Funny Nerd Agent**: Generates nerdy jokes on topics like programming, math, and science.
- **News Analyst Agent**: Searches and summarizes news articles using Google Search.
- **Stock Analyst Agent**: Fetches and displays current stock prices using the `yfinance` library.

The system also includes utility tools like fetching the current time, which can be used by agents for time-sensitive tasks.

---

## 📂 Project Structure

The project is organized under the `Chapter-06` directory with the following structure:

```
Chapter-06/
├── manager/                    # Root manager agent module
│   ├── agent.py                # Defines the manager agent for task delegation
│   └── __init__.py             # Initializes the manager module
├── Sub_agents/                 # Sub-agents for specific tasks
│   ├── funny_nerd/             # Funny Nerd Agent module
│   │   └── agent.py            # Implements the agent for nerdy jokes
│   ├── news_analyst/           # News Analyst Agent module
│   │   └── agent.py            # Implements the agent for news analysis
│   └── stock_analyst/          # Stock Analyst Agent module
│       └── agent.py            # Implements the agent for stock price fetching
├── .env                        # Environment variables (e.g., API keys)
└── __init__.py                 # Initializes the project root
```

---

## 🛠️ Code Overview with Examples

### 1. Funny Nerd Agent
The `funny_nerd` agent generates nerdy jokes based on a given topic. It validates the topic and then crafts a joke.

**Example Code** (from `Sub_agents/funny_nerd/agent.py`):
```python
def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    valid_topics = ["python", "javascript", "java", "programming", "math", "physics", "chemistry", "biology"]
    if topic.lower() not in valid_topics:
        return {
            "status": "error",
            "message": f"'{topic}' is not a supported topic.",
            "supported_topics": valid_topics
        }
    tool_context.state["last_joke_topic"] = topic
    return {"status": "ok", "topic": topic}
```

**Usage Example**:
If a user requests a joke about "python", the agent validates the topic and might respond with:
```
Here's a nerdy joke about python:
Why did the Python programmer prefer dark mode? Because the light attracts bugs.

Explanation: In Python, "bugs" refer to coding errors, and dark mode reduces eye strain for programmers.
```

---

### 2. News Analyst Agent
The `news_analyst` agent searches for news articles and summarizes them using the `google_search` tool.

**Example Code** (from `Sub_agents/news_analyst/agent.py`):
```python
news_analyst = Agent(
    name="news_analyst",
    model="gemini-2.0-flash",
    description="News analyst agent",
    instruction="""
    You are a helpful assistant that can analyze news articles and provide a summary of the news.
    When asked about news, you should use the google_search tool to search for the news.
    """,
    tools=[google_search],
)
```

**Usage Example**:
If a user asks for news about "AI advancements today", the agent might search and summarize:
```
Recent AI advancements include a new model by xAI that improves reasoning capabilities, released on May 19, 2025.
```

---

### 3. Stock Analyst Agent
The `stock_analyst` agent fetches current stock prices using the `yfinance` library.

**Example Code** (from `Sub_agents/stock_analyst/agent.py`):
```python
def get_stock_price(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")
        if current_price is None:
            return {"status": "error", "error_message": f"Could not fetch price for {ticker}"}
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": current_time,
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Error fetching stock data: {str(e)}"}
```

**Usage Example**:
If a user asks for the stock price of "GOOG", the agent might respond:
```
Here are the current prices for your stocks:
- GOOG: $175.34 (updated at 2025-05-19 17:27:00)
```

---

### 4. Manager Agent
The `manager` agent delegates tasks to the appropriate sub-agents.

**Example Code** (from `manager/agent.py`):
```python
root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.
    Always delegate the task to the appropriate agent.
    """,
    sub_agents=[stock_analyst, funny_nerd],
    tools=[AgentTool(news_analyst), get_current_time]
)
```

**Usage Example**:
If a user asks, "Tell me a nerdy joke about math," the manager delegates to the `funny_nerd` agent.

---

## 🏃 How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Install required packages:
  ```bash
  pip install python-dotenv google-adk yfinance
  ```
- Set up a `.env` file in the project root with necessary API keys (e.g., for `google.adk`).

### Steps to Run
1. Clone the repository or navigate to the `Chapter-06` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If a `requirements.txt` is not present, use the command under Prerequisites.)
3. Ensure the `.env` file is configured with required environment variables.
4. Run the main agent:
   ```bash
   python manager/agent.py
   ```
5. Interact with the system by sending requests to the manager agent (e.g., via a client or API interface).

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

**Built with ❤️ by the Sadi_AI Community**
