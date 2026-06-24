"""
ui.py
-----
Builds the Panel UI and wires every button to its handler.
All business logic is delegated to the other modules; this file only
knows about widgets, layout, and how to plumb them together.
"""

import panel as pn
from tornado.iostream import StreamClosedError
from tornado.websocket import WebSocketClosedError

from config import (
    DIAGRAM_SYSTEM_PROMPT,
    PANE_STYLE, TITLE_STYLE, SECTION_STYLE, INPUT_STYLE, BUTTON_STYLE,
)
from llm_client import stream_to_pane, strip_fences
from state import get_conversation, reset_conversation
from note_generator import generate_engineering_note
from pdf_renderer import render_report_pdf, render_engineering_note_pdf


# ── Safe pane update ──────────────────────────────────────────────────────────

def _safe_set(pane, text: str) -> bool:
    try:
        pane.object = text
        return True
    except (WebSocketClosedError, StreamClosedError):
        return False


# ── UI factory ────────────────────────────────────────────────────────────────

def build_ui() -> pn.Column:
    """Construct and return the complete application layout."""

    # ── Widgets ───────────────────────────────────────────────────────────────
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
        name="⚡ Debug", button_type="primary", width=200, height=50, styles=BUTTON_STYLE
    )
    diagram_btn = pn.widgets.Button(
        name="📊 Diagram", button_type="warning", width=200, height=50, styles=BUTTON_STYLE
    )
    followup_btn = pn.widgets.Button(
        name="💬 Follow-Up", button_type="success", width=200, height=50, styles=BUTTON_STYLE
    )
    reset_btn = pn.widgets.Button(
        name="🗑️ Reset", button_type="danger", width=200, height=50, styles=BUTTON_STYLE
    )

    # ── Event handlers ────────────────────────────────────────────────────────

    def on_debug(_):
        code = code_input.value.strip()
        if not code:
            _safe_set(output, "Please enter some Python code.")
            return
        conv = get_conversation()
        conv.append({"role": "user", "content": code})
        _safe_set(output, "_Analysing…_")
        stream_to_pane(conv, output)

    def on_diagram(_):
        code = code_input.value.strip()
        if not code:
            _safe_set(diagram_output, "Please enter some Python code first.")
            return

        conv = get_conversation()
        last_assistant = next(
            (m["content"] for m in reversed(conv) if m["role"] == "assistant"),
            None,
        )

        payload = [
            {"role": "system", "content": DIAGRAM_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Code:\n```python\n{code}\n```"
                    + (f"\n\nAnalysis:\n{last_assistant}" if last_assistant else "")
                ),
            },
        ]

        def _wrap_as_codeblock(text: str) -> str:
            return f"```\n{strip_fences(text)}\n```"

        _safe_set(diagram_output, "_Generating diagrams…_")
        stream_to_pane(payload, diagram_output, post_process=_wrap_as_codeblock)

    def on_followup(_):
        q = followup_input.value.strip()
        if not q:
            _safe_set(output, "Please enter a question.")
            return
        conv = get_conversation()
        conv.append({"role": "user", "content": q})
        _safe_set(output, "_Thinking…_")
        stream_to_pane(conv, output)

    def on_reset(_):
        reset_conversation()
        _safe_set(output, "_Analysis will appear here..._")
        _safe_set(diagram_output, "_Diagrams will appear here..._")
        followup_input.value = ""
        code_input.value = ""

    def on_download():
        code     = code_input.value.strip()
        analysis = output.object or ""
        diagrams = strip_fences(diagram_output.object or "")
        return render_report_pdf(code, analysis, diagrams)

    def on_engineering_note():
        code = code_input.value.strip()
        if not code:
            return render_engineering_note_pdf("", "No code provided.", "")
        analysis = output.object or ""
        diagrams  = strip_fences(diagram_output.object or "")
        note_text = generate_engineering_note(code, analysis, diagrams)
        return render_engineering_note_pdf(code, note_text, diagrams)

    # ── Wire buttons ──────────────────────────────────────────────────────────
    debug_btn.on_click(on_debug)
    diagram_btn.on_click(on_diagram)
    followup_btn.on_click(on_followup)
    reset_btn.on_click(on_reset)

    download_btn = pn.widgets.FileDownload(
        callback=on_download,
        filename="debug_report.pdf",
        label="📥 Download Report",
        button_type="success",
        width=220,
        height=50,
    )

    engineering_note_btn = pn.widgets.FileDownload(
        callback=on_engineering_note,
        filename="engineering_note_python_debugging_review.pdf",
        label="🧾 Download Engineering Note",
        button_type="primary",
        width=260,
        height=50,
    )

    # ── Layout ────────────────────────────────────────────────────────────────
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
        pn.Row(followup_btn, reset_btn, download_btn, engineering_note_btn),
        sizing_mode="stretch_width",
    )
