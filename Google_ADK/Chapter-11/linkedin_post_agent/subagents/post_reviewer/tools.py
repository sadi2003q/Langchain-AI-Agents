from google.adk.tools.tool_context import ToolContext
from typing import Any, Dict


def count_characters(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Validates the length of the input text based on character count constraints.

    :param text: The input text to be evaluated.
    :param tool_context: The context in which this tool operates, used for updating state.
    :return: A dictionary containing the status, character count, and a message.
    """

    max_character = 1500
    min_character = 1000
    char_count = len(text.split())

    if char_count>max_character:
        tool_context.state['review_status'] = 'failed'
        character_to_remove = char_count-max_character
        return {
            'status': 'failed',
            'character_count': char_count,
            'character_to_remove': character_to_remove,
            'message': f'Post is too long, Please remove {character_to_remove} to meet the maximum length of {max_character}'
        }
    elif char_count<min_character:
        tool_context.state['review_status'] = 'failed'
        character_needed = char_count-min_character
        return {
            'status': 'failed',
            'character_count': char_count,
            'character_needed': character_needed,
            'message': f'Post is too short, Please add {character_needed} to meet the minimum length of {min_character}'
        }
    else:
        tool_context.state['review_status'] = 'success'
        return {
            'status': 'success',
            'character_count': char_count,
            'message': f"Post length is good ({char_count} characters).",
        }


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
       Call this function ONLY when the post meets all quality requirements,
       signaling the iterative process should end.

       Args:
           tool_context: Context for tool execution

       Returns:
           Empty dictionary
    """
    tool_context.actions.escalate = True
    return {}
