"""
note_generator.py
-----------------
Generates the *text* of an engineering note by calling the LLM.
Kept separate from pdf_renderer (which turns text into bytes) and from
llm_client (which knows nothing about prompts).
"""

from config import ENGINEERING_NOTE_PROMPT
from llm_client import generate_text


def generate_engineering_note(code: str, analysis: str, diagrams: str) -> str:
    """
    Ask the LLM to write a formal engineering note and return it as a string.

    Parameters
    ----------
    code     : The fixed Python code.
    analysis : The prior debugging analysis from the main conversation.
    diagrams : ASCII flow-chart text (may be empty).
    """
    messages = [
        {"role": "system", "content": ENGINEERING_NOTE_PROMPT},
        {
            "role": "user",
            "content": (
                f"Fixed code:\n```python\n{code}\n```\n\n"
                f"Analysis:\n{analysis}\n\n"
                f"Diagrams:\n{diagrams}"
            ),
        },
    ]
    return generate_text(messages)
