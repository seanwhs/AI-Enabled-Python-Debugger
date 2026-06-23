import os
import threading
from dataclasses import dataclass
from typing import List, Dict, Optional

from dotenv import load_dotenv
import panel as pn
from openai import OpenAI
from tornado.iostream import StreamClosedError
from tornado.websocket import WebSocketClosedError

load_dotenv()

pn.extension("codeeditor", sizing_mode="stretch_width", design="bootstrap")

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

DIAGRAM_SYSTEM_PROMPT = """You are a software architecture expert.
Generate TWO ASCII flowcharts, each wrapped in triple-backtick fenced code blocks.
Label the first "Buggy Code Flow" and the second "Fixed Code Flow" inside the block.
Use only ASCII characters: [], -->, |, and spaces for indentation.
Do not add any prose, headers, or explanation outside the two code blocks.
"""

MODELS_POOL = [
    "openai/gpt-oss-20b:free",
    "cohere/north-mini-code:free",
    "meta-llama/llama-3.2-3b-instruct:free",
]

SESSION_KEY = "session_id"
DEFAULT_SESSION = "default"

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

TITLE_STYLE = {"font-size": "32px"}
SECTION_STYLE = {"font-size": "24px"}
INPUT_STYLE = {"font-size": "18px"}
BUTTON_STYLE = {"font-size": "18px"}

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger",
        "X-Title": "AI Enabled Python Debugger",
    },
)


@dataclass
class AppState:
    system_prompt: str = SYSTEM_PROMPT
    cache_key: str = DEFAULT_SESSION


def get_session_id() -> str:
    return pn.state.session_args.get(SESSION_KEY, [DEFAULT_SESSION])[0]


def get_conv() -> List[Dict[str, str]]:
    sid = get_session_id()
    if sid not in pn.state.cache:
        pn.state.cache[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return pn.state.cache[sid]


def safe_set(pane, text: str) -> bool:
    try:
        pane.object = text
        return True
    except (WebSocketClosedError, StreamClosedError):
        return False


def call_llm(messages, stream: bool = False):
    last_error = None
    for model in MODELS_POOL:
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2048,
                stream=stream,
            )
        except Exception as e:
            last_error = e
    raise RuntimeError(f"All models failed: {last_error}")


def stream_to_pane(messages: list, pane) -> None:
    def _run():
        try:
            stream = call_llm(messages, stream=True)
        except Exception as e:
            safe_set(pane, f"**Error:** {e}")
            return

        full = ""
        try:
            for chunk in stream:
                bit = getattr(chunk.choices[0].delta, "content", None)
                if not bit:
                    continue
                full += bit
                if not safe_set(pane, full):
                    return
        except (WebSocketClosedError, StreamClosedError):
            return
        except Exception as e:
            safe_set(pane, f"**Error:** {e}")
            return

        messages.append({"role": "assistant", "content": full})

    threading.Thread(target=_run, daemon=True).start()


def build_ui():
    code_input = pn.widgets.CodeEditor(
        language="python",
        height=300,
        theme="monokai",
        sizing_mode="stretch_width",
        margin=(10, 0, 15, 0),
    )

    output = pn.pane.Markdown("_Analysis will appear here..._", sizing_mode="stretch_width", styles=PANE_STYLE)
    diagram_output = pn.pane.Markdown("_Diagrams will appear here..._", sizing_mode="stretch_width", styles=PANE_STYLE)
    followup_input = pn.widgets.TextInput(
        placeholder="Ask a follow-up question...",
        sizing_mode="stretch_width",
        styles=INPUT_STYLE,
    )

    debug_btn = pn.widgets.Button(name="⚡ Debug", button_type="primary", width=200, height=50, styles=BUTTON_STYLE)
    diagram_btn = pn.widgets.Button(name="📊 Diagram", button_type="warning", width=200, height=50, styles=BUTTON_STYLE)
    followup_btn = pn.widgets.Button(name="💬 Follow-Up", button_type="success", width=200, height=50, styles=BUTTON_STYLE)
    reset_btn = pn.widgets.Button(name="🗑️ Reset", button_type="danger", width=200, height=50, styles=BUTTON_STYLE)

    def on_debug(_):
        code = code_input.value.strip()
        if not code:
            safe_set(output, "Please enter some Python code.")
            return
        conv = get_conv()
        conv.append({"role": "user", "content": code})
        safe_set(output, "_Analyzing…_")
        stream_to_pane(conv, output)

    def on_diagram(_):
        code = code_input.value.strip()
        if not code:
            safe_set(diagram_output, "Please enter some Python code first.")
            return

        conv = get_conv()
        last = next((m["content"] for m in reversed(conv) if m["role"] == "assistant"), None)
        payload = [
            {"role": "system", "content": DIAGRAM_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Code:\n```python\n{code}\n```" + (f"\n\nAnalysis:\n{last}" if last else ""),
            },
        ]
        safe_set(diagram_output, "_Generating diagrams…_")
        stream_to_pane(payload, diagram_output)

    def on_followup(_):
        q = followup_input.value.strip()
        if not q:
            safe_set(output, "Please enter a question.")
            return
        conv = get_conv()
        conv.append({"role": "user", "content": q})
        safe_set(output, "_Thinking…_")
        stream_to_pane(conv, output)

    def on_reset(_):
        sid = get_session_id()
        pn.state.cache[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
        safe_set(output, "_Analysis will appear here..._")
        safe_set(diagram_output, "_Diagrams will appear here..._")
        followup_input.value = ""
        code_input.value = ""

    debug_btn.on_click(on_debug)
    diagram_btn.on_click(on_diagram)
    followup_btn.on_click(on_followup)
    reset_btn.on_click(on_reset)

    return pn.Column(
        pn.pane.Markdown("# 🐍 AI Python Debugger", styles=TITLE_STYLE),
        code_input,
        pn.Row(debug_btn, diagram_btn),
        pn.layout.Divider(),
        pn.pane.Markdown("## Analysis", styles=SECTION_STYLE),
        output,
        pn.layout.Divider(),
        pn.pane.Markdown("## Diagrams", styles=SECTION_STYLE),
        diagram_output,
        pn.layout.Divider(),
        pn.pane.Markdown("## Follow-up", styles=SECTION_STYLE),
        followup_input,
        pn.Row(followup_btn, reset_btn),
        sizing_mode="stretch_width",
    )


app = build_ui()
app.servable()