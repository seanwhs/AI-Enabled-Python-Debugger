"""
config.py
---------
All static configuration: prompts, model pool, and UI style constants.
Nothing here has side-effects; import freely from any module.
"""

SYSTEM_PROMPT = """You are an expert Python debugging assistant.
When given Python code:
1. Identify the bug.
2. Explain the root cause.
3. Provide fixed code.
4. Suggest unit tests.

Return your answer using these Markdown sections:
## Error
## Explanation
## Fixed Code
## Unit Tests
## Improvements
"""

ENGINEERING_NOTE_PROMPT = """You are an expert software engineer writing concise engineering notes.

Create a professional engineering note for the fixed code with these sections:
## Title
## Problem Summary
## Root Cause
## Fix Applied
## Validation
## Notes

Rules:
- Write in clear, formal engineering language.
- Focus on the corrected behavior and why the fix works.
- Keep it practical and implementation-focused.
- Mention any edge cases or follow-up improvements if relevant.
- Do not include fluff or generic advice.
- Use a title appropriate for a technical postmortem or internal engineering note.
"""

DIAGRAM_SYSTEM_PROMPT = """You are a software process expert.
Generate TWO ASCII flow charts using box-drawing characters that represent algorithmic control flow rather than static architectural components.
Label the first "=== Buggy Code Flow =" and the second "= Fixed Code Flow ===".

Use these symbols for flow logic:
+-------+   for process steps
<       >   for decision diamonds
+-->        for horizontal paths
|           for vertical paths
v           for directional flow

Example style:
+-----------+
| Initialize|
+-----+-----+
|
v
+-----+-----+       +-----------+
|   Loop    +------>| Process   |
+-----+-----+       +-----+-----+
|                   |
v                   v
+-----------+       +-----------+
|  Finish   |<------+   Done    |
+-----------+       +-----------+

Wrap each diagram in a triple-backtick plain code block.
Do not add any prose or explanation outside the two code blocks.
"""

MODELS_POOL = [
    # OpenAI
    "openai/gpt-oss-20b:free",

    # Qwen
    "qwen/qwen3-coder:free",

    # Google
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",

    # NVIDIA
    "nvidia/nemotron-3-ultra-550b-a55b:free",

    # Poolside
    "poolside/laguna-xs.2:free",

    # Nous Research
    "nousresearch/hermes-3-llama-3.1-405b:free",

    # Meta
    "meta-llama/llama-3.3-70b-instruct:free",

    # Z AI
    "z-ai/glm-4.5-air:free",

    # OpenAI (larger)
    "openai/gpt-oss-120b:free",
]

# ── UI style dicts ────────────────────────────────────────────────────────────

PANE_STYLE = {
    "font-size": "20px",
    "line-height": "1.9",
    "width": "100%",
    "background-color": "#111827",
    "color": "#f9fafb",
    "padding": "16px",
    "border-radius": "10px",
    "border": "1px solid #374151",
}

TITLE_STYLE   = {"font-size": "32px"}
SECTION_STYLE = {"font-size": "24px"}
INPUT_STYLE   = {"font-size": "18px"}
BUTTON_STYLE  = {"font-size": "18px"}
