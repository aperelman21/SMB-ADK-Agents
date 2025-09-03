import logging
import os
from datetime import datetime
from typing import Any
from google.adk.tools.tool_context import ToolContext

def set_state_value(
    tool_context: ToolContext, field: str, value: str
) -> dict[str, str]:
    """Set a value for a key in the shared state. Overwrites existing value.

    Args:
        field (str): The field name (key) to set in the state.
        value (str): The string value to set for the field.

    Returns:
        dict[str, str]: {"status": "success"}
    """
    tool_context.state[field] = value
    logging.info(f"[State Set] {field}: {value}")
    return {"status": "success"}

def get_state_value(
    tool_context: ToolContext, field: str
) -> dict[str, Any]:
    """Get a value for a key from the shared state.

    Args:
        field (str): The field name (key) to get from the state.

    Returns:
        dict[str, Any]: A dictionary containing the value from the state.
    """
    value = tool_context.state.get(field)
    logging.info(f"[State Get] {field}: {value}")
    return {"value": value}