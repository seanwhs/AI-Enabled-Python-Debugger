import os  # Access environment variables (e.g. API keys)
import io  # In-memory file buffers for PDF download
import html  # Escape text for safe PDF rendering
import threading  # Run LLM streaming in a background thread
import re  # Strip code fences from diagram output
from dataclasses import dataclass  # Simple container for application state
from typing import List, Dict, Optional  # Type hints

from dotenv import load_dotenv  # Load variables from .env
import panel as pn  # Panel framework for building the web UI
from openai import OpenAI  # OpenAI-compatible client (used with OpenRouter)
from tornado.iostream import StreamClosedError  # Raised when browser disconnects
from tornado.websocket import WebSocketClosedError  # Raised when websocket closes

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors


load_dotenv()  # Load environment variables from .env into the process
pn.extension("codeeditor", sizing_mode="stretch_width", design="bootstrap")  # Initialize Panel UI components


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

SESSION_KEY = "session_id"  # Session identifier used by Panel
DEFAULT_SESSION = "default"  # Fallback session id

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


TITLE_STYLE = {"font-size": "32px"}  # Title text styling
SECTION_STYLE = {"font-size": "24px"}  # Section header styling
INPUT_STYLE = {"font-size": "18px"}  # Input widget styling
BUTTON_STYLE = {"font-size": "18px"}  # Button widget styling


client = OpenAI(  # OpenAI-compatible client configured for OpenRouter
    api_key=os.getenv("OPENROUTER_API_KEY"),  # API key stored in environment
    base_url="https://openrouter.ai/api/v1",  # OpenRouter API endpoint
    default_headers={  # Optional metadata shown by OpenRouter
        "HTTP-Referer": "https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger",
        "X-Title": "AI Enabled Python Debugger",
    },
)


@dataclass
class AppState:
    system_prompt: str = SYSTEM_PROMPT
    cache_key: str = DEFAULT_SESSION


def get_session_id() -> str:
    """Return the current browser session ID."""
    return pn.state.session_args.get(SESSION_KEY, [DEFAULT_SESSION])[0]


def get_conv() -> List[Dict[str, str]]:
    """
    Retrieve the current conversation history.
    Creates a new conversation if one doesn't exist.
    """
    sid = get_session_id()
    if sid not in pn.state.cache:  # Initialize conversation on first use
        pn.state.cache[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return pn.state.cache[sid]


def safe_set(pane, text: str) -> bool:
    """
    Safely update a Panel pane.
    Returns False if the browser has disconnected.
    """
    try:
        pane.object = text
        return True
    except (WebSocketClosedError, StreamClosedError):
        return False


def call_llm(messages, stream: bool = False):
    """
    Send messages to the LLM.
    Automatically retries using fallback models if one fails.
    """
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


def strip_fences(text: str) -> str:
    """Remove all triple-backtick fences from model output."""
    return re.sub(r"```[a-zA-Z0-9_-]*\n?", "", text).strip()


def stream_to_pane(messages: list, pane, post_process=None) -> None:
    """
    Stream the model response into a pane without blocking the UI.
    Optional post_process(text) -> text applied after streaming completes.
    """
    def _run():
        try:
            stream = call_llm(messages, stream=True)  # Begin streaming from the LLM
        except Exception as e:
            safe_set(pane, f"**Error:** {e}")
            return

        full = ""
        try:
            for chunk in stream:
                bit = getattr(chunk.choices[0].delta, "content", None)
                if not bit:  # Ignore empty chunks
                    continue
                full += bit
                if not safe_set(pane, full):  # Stop if browser disconnects
                    return
        except (WebSocketClosedError, StreamClosedError):
            return
        except Exception as e:
            safe_set(pane, f"**Error:** {e}")
            return

        if post_process:  # Apply cleanup after streaming completes
            full = post_process(full)
            safe_set(pane, full)

        messages.append({"role": "assistant", "content": full})  # Save assistant response

    threading.Thread(target=_run, daemon=True).start()  # Run streaming in the background


def generate_text(messages: list) -> str:
    """Generate a non-streaming LLM response."""
    resp = call_llm(messages, stream=False)
    return resp.choices[0].message.content or ""


def render_report_pdf(original_code: str, analysis_text: str, diagram_text: str) -> io.BytesIO:
    """Create a PDF report containing code, analysis, and architecture diagrams."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    code_style = ParagraphStyle(
        "CodeBlock",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor("#111827"),
        backColor=colors.HexColor("#f3f4f6"),
        borderPadding=6,
        spaceAfter=10,
        alignment=TA_LEFT,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        spaceAfter=6,
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#111827"),
        spaceBefore=10,
        spaceAfter=8,
    )

    story = [
        Paragraph("AI Python Debugger Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph("Original Buggy Code", heading_style),
        Preformatted(original_code, code_style),
        Paragraph("Analysis", heading_style),
    ]

    for line in analysis_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            story.append(Paragraph(html.escape(line[3:]), heading_style))
        else:
            story.append(Paragraph(html.escape(line).replace("\n", "<br/>"), body_style))

    story.append(Paragraph("Architecture Diagrams", heading_style))
    story.append(Preformatted(diagram_text or "No diagrams available.", code_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


def build_ui():
    """Build and return the complete application interface."""
    code_input = pn.widgets.CodeEditor(
        language="python",
        height=300,
        theme="monokai",
        sizing_mode="stretch_width",
        margin=(10, 0, 15, 0),
    )

    output = pn.pane.Markdown(
        "_Analysis will appear here..._",
        sizing_mode="stretch_width",
        styles=PANE_STYLE,
    )

    diagram_output = pn.pane.Markdown(
        "_Diagrams will appear here..._",
        sizing_mode="stretch_width",
        styles=PANE_STYLE,
    )

    followup_input = pn.widgets.TextInput(
        placeholder="Ask a follow-up question...",
        sizing_mode="stretch_width",
        styles=INPUT_STYLE,
    )

    debug_btn = pn.widgets.Button(
        name="⚡ Debug",
        button_type="primary",
        width=200,
        height=50,
        styles=BUTTON_STYLE,
    )

    diagram_btn = pn.widgets.Button(
        name="📊 Diagram",
        button_type="warning",
        width=200,
        height=50,
        styles=BUTTON_STYLE,
    )

    followup_btn = pn.widgets.Button(
        name="💬 Follow-Up",
        button_type="success",
        width=200,
        height=50,
        styles=BUTTON_STYLE,
    )

    reset_btn = pn.widgets.Button(
        name="🗑️ Reset",
        button_type="danger",
        width=200,
        height=50,
        styles=BUTTON_STYLE,
    )

    def on_debug(_):
        """Handle Debug button click."""
        code = code_input.value.strip()
        if not code:
            safe_set(output, "Please enter some Python code.")
            return

        conv = get_conv()  # Add user code to conversation history
        conv.append({"role": "user", "content": code})
        safe_set(output, "_Analyzing…_")
        stream_to_pane(conv, output)  # Stream AI response

    def on_diagram(_):
        """Generate ASCII architecture diagrams."""
        code = code_input.value.strip()
        if not code:
            safe_set(diagram_output, "Please enter some Python code first.")
            return

        conv = get_conv()
        last = next(
            (m["content"] for m in reversed(conv) if m["role"] == "assistant"),
            None,
        )

        payload = [
            {"role": "system", "content": DIAGRAM_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Code:\n```python\n{code}\n```"
                    + (f"\n\nAnalysis:\n{last}" if last else "")
                ),
            },
        ]

        def wrap_as_codeblock(text: str) -> str:
            """Strip fences then re-wrap so Markdown renders as preformatted monospace."""
            cleaned = strip_fences(text)
            return f"```\n{cleaned}\n```"

        safe_set(diagram_output, "_Generating diagrams…_")
        stream_to_pane(payload, diagram_output, post_process=wrap_as_codeblock)

    def on_followup(_):
        """Handle follow-up questions."""
        q = followup_input.value.strip()
        if not q:
            safe_set(output, "Please enter a question.")
            return

        conv = get_conv()
        conv.append({"role": "user", "content": q})  # Continue the existing conversation
        safe_set(output, "_Thinking…_")
        stream_to_pane(conv, output)

    def on_reset(_):
        """Reset the application state."""
        sid = get_session_id()
        pn.state.cache[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]  # Start a fresh conversation
        safe_set(output, "_Analysis will appear here..._")
        safe_set(diagram_output, "_Diagrams will appear here..._")
        followup_input.value = ""
        code_input.value = ""

    def on_download():
        """Generate the PDF report when the user clicks download."""
        code = code_input.value.strip()
        analysis = output.object or ""
        diagrams = strip_fences(diagram_output.object or "")  # strip_fences handles the wrapper fence too
        return render_report_pdf(code, analysis, diagrams)

    debug_btn.on_click(on_debug)      # Wire Debug button
    diagram_btn.on_click(on_diagram)  # Wire Diagram button
    followup_btn.on_click(on_followup)  # Wire Follow-Up button
    reset_btn.on_click(on_reset)      # Wire Reset button

    download_btn = pn.widgets.FileDownload(
        callback=on_download,
        filename="debug_report.pdf",
        label="📥 Download Report",
        button_type="success",
        width=220,
        height=50,
    )

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
        pn.Row(followup_btn, reset_btn, download_btn),
        sizing_mode="stretch_width",
    )


app = build_ui()   # Build the application
app.servable()     # Make the application available when served by Panel