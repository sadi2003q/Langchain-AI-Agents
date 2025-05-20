import copy
from google.adk.agents import LlmAgent
from datetime import datetime
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
from litellm.integrations.galileo import LLMResponse


def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    state = callback_context.state

    last_user_message = ""
    if llm_request.contents and len(llm_request.contents) > 0:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts and len(content.parts) > 0:
                if hasattr(content.parts[0], "text") and content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    if last_user_message:
        state["last_user_message"] = last_user_message

    if last_user_message and "sucks" in last_user_message.lower():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="I cannot respond to messages containing inappropriate language"
                    )
                ]
            )
        )

    state["model_start_time"] = datetime.now()
    return None


def after_model_callback(llm_response:LLMResponse) -> Optional[LlmResponse]:
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None

    response_text = ""
    for part in llm_response.content.parts:
        if hasattr(part, "text") and part.text:
            response_text += part.text

    if not response_text:
        return None

    replacements = {
        "problem": "challenge",
        "difficult": "complex",
    }

    # Perform replacements
    modified_text = response_text
    modified = False

    for original, replacement in replacements.items():
        if original in modified_text.lower():
            modified_text = modified_text.replace(original, replacement)
            modified_text = modified_text.replace(
                original.capitalize(), replacement.capitalize()
            )
            modified = True
    if modified:

        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        for i, part in enumerate(modified_parts):
            if hasattr(part, "text") and part.text:
                modified_parts[i].text = modified_text

        return LlmResponse(content=types.Content(role="model", parts=modified_parts))

    return None


root_agent = LlmAgent(
    name="content_filter_agent",
    model="gemini-2.0-flash",
    description="An agent that demonstrates model callbacks for content filtering and logging",
    instruction="""
    You are a helpful assistant.

    Your job is to:
    - Answer user questions concisely
    - Provide factual information
    - Be friendly and respectful
    """,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
