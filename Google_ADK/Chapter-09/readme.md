# 📊 Lead Qualification System

Welcome to the **Lead Qualification System**! This project is a Python-based application that automates the qualification process for sales leads using a sequential agent pipeline built with the `google.adk` framework. It validates lead information, scores leads based on key criteria, and recommends the next sales actions.

---

## 🚀 Project Overview

The project implements a multi-step lead qualification pipeline with three specialized sub-agents:

- **Validator Agent**: Checks if lead information is complete (e.g., contact details, interest).
- **Scorer Agent**: Assigns a qualification score (1-10) based on need, authority, budget, and timeline.
- **Recommender Agent**: Suggests tailored sales actions based on the lead's score and validation status.

The system processes leads sequentially, ensuring a structured approach to lead management, making it ideal for sales teams looking to prioritize and engage effectively.

---

## 📂 Project Structure

The project is organized under the `Chapter-09` directory with the following structure:

```
Chapter-09/
├── load_qualification_agent/    # Main lead qualification agent module
│   ├── subagents/              # Sub-agents for specific tasks
│   │   ├── recommender/        # Recommender Agent module
│   │   │   ├── __init__.py     # Initializes the module
│   │   │   └── agent.py        # Implements the agent for action recommendations
│   │   ├── scorer/             # Scorer Agent module
│   │   │   ├── __init__.py     # Initializes the module
│   │   │   └── agent.py        # Implements the agent for lead scoring
│   │   └── validator/          # Validator Agent module
│   │       ├── __init__.py     # Initializes the module
│   │       └── agent.py        # Implements the agent for lead validation
│   ├── .env                    # Environment variables (e.g., API keys)
│   ├── __init__.py             # Initializes the module
│   └── agent.py                # Defines the sequential agent pipeline
```

---

## 🛠️ Code Overview with Examples

### 1. Validator Agent
The `validator` agent checks if lead information is complete.

**Example Code** (from `subagents/validator/agent.py`):
```python
lead_validator_agent = Agent(
    name="validator",
    model="gemini-2.0-flash",
    description="Validates Lead information for completeness",
    instruction="""
    You are a Lead Validation AI.
    
    Examine the lead information provided by the user and determine if it's complete enough for qualification.
    A complete lead should include:
    - Contact information (name, email or phone)
    - Some indication of interest or need
    - Company or context information if applicable
    
    Output ONLY 'valid' or 'invalid' with a single reason if invalid.
    
    Example valid output: 'valid'
    Example invalid output: 'invalid: missing contact information'
    """,
    output_key="validation_status",
)
```

**Explanation**:
- Validates lead data against required fields (contact, interest, context).
- Outputs a simple `valid` or `invalid` status with a reason if invalid.

**Usage Example**:
If a lead provides no contact info, the output might be:
```
invalid: missing contact information
```

---

### 2. Scorer Agent
The `scorer` agent assigns a score (1-10) based on lead quality.

**Example Code** (from `subagents/scorer/agent.py`):
```python
lead_score_agent = Agent(
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
```

**Explanation**:
- Evaluates lead quality using four criteria: need, authority, budget, and timeline.
- Returns a single score with a concise justification.

**Usage Example**:
For a lead with clear needs and budget, the output might be:
```
8: Decision maker with clear budget and immediate need
```

---

### 3. Recommender Agent
The `recommender` agent suggests sales actions based on the score and validation status.

**Example Code** (from `subagents/recommender/agent.py`):
```python
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
```

**Explanation**:
- Uses the validation status and score to recommend tailored actions.
- Provides a formatted recommendation for the sales team.

**Usage Example**:
For a valid lead with a score of 9, the output might be:
```
Recommendation: Proceed with a product demo and prepare a tailored proposal for the sales team, as the lead is highly qualified with a score of 9.
```

---

### 4. Root Agent (Sequential Pipeline)
The `load_qualification_agent` orchestrates the sub-agents in sequence.

**Example Code** (from `agent.py`):
```python
root_agent = SequentialAgent(
    name="load_qualification_agent",
    sub_agents=[lead_validator_agent, lead_score_agent, action_recommendation_agent],
    description="A pipeline that validates, scores and recommends actions for sales leads"
)
```

**Explanation**:
- Combines the validator, scorer, and recommender agents into a single pipeline.
- Processes lead data in order: validation → scoring → recommendation.

**Usage Example**:
Input: A lead with contact info and urgent need.
Output: Validates as `valid`, scores `8`, and recommends a demo.

---

## 🏃 How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Install required packages:
  ```bash
  pip install python-dotenv google-adk
  ```
- Set up a `.env` file in the `load_qualification_agent` directory with necessary API keys (e.g., for `google.adk`).

### Steps to Run
1. Clone the repository or navigate to the `Chapter-09` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If a `requirements.txt` is not present, use the command under Prerequisites.)
3. Navigate to the `load_qualification_agent` directory:
   ```bash
   cd load_qualification_agent
   ```
4. Ensure the `.env` file is configured with required environment variables.
5. Run the agent (requires integration with a runner or client):
   ```bash
   python agent.py
   ```
   **Note**: This project is a pipeline demo and requires a client or runner (e.g., from `google.adk`) to process lead data interactively.

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

**Built with ❤️ by the sadi_AI Community**
