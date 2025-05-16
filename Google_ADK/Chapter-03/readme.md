# Structuring Data in LLM Agents (Google ADK)

This document summarizes the structure and purpose of the `input_schema`, `output_schema`, and `output_key` parameters used for structured data exchange in Google ADK LLM agents. These parameters help define how data is passed into and out of agents using Pydantic models.

---

## 📥 `input_schema` (Optional)

- Defines the **expected input structure** using a `Pydantic BaseModel`.
- If set, the user's input must be a **JSON string** that matches this schema.
- Use this to guide either the user or the **preceding agent** to ensure valid input.

---

## 📤 `output_schema` (Optional)

- Defines the **expected output structure** using a `Pydantic BaseModel`.
- If set, the agent's **final response** must be a JSON string conforming to this schema.

**⚠️ Constraint:**
- Enabling `output_schema` allows the LLM to generate controlled output.
- However, it **disables the agent's ability to:**
  - Use tools
  - Transfer control to other agents
- Instructions must guide the LLM to **directly output** the matching JSON.

---

## 🗝️ `output_key` (Optional)

- Defines a key for storing the **final text output** in the session's state dictionary.
- Usage: `session.state[output_key] = agent_response_text`
- Useful for **passing results** between agents or steps in a workflow.

---

### Summary

These parameters help enforce structure, validity, and flow in multi-agent LLM systems. Use them to ensure data is validated and properly routed throughout your application.