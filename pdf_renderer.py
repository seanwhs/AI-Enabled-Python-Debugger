"""
pdf_renderer.py
---------------
Responsible solely for turning text content into PDF byte buffers.
Two public functions, one per document type:
  - render_report_pdf          – full debug report (code + analysis + diagrams)
  - render_engineering_note_pdf – formal engineering note
"""

import html
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted


# ── Shared style factory ──────────────────────────────────────────────────────

def _build_styles():
    """Return a dict of named ParagraphStyle objects used by both renderers."""
    base = getSampleStyleSheet()

    code = ParagraphStyle(
        "CodeBlock",
        parent=base["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor("#111827"),
        backColor=colors.HexColor("#f3f4f6"),
        borderPadding=6,
        spaceAfter=10,
        alignment=TA_LEFT,
    )

    body = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontSize=10,
        leading=13,
        spaceAfter=6,
    )

    heading = ParagraphStyle(
        "Heading",
        parent=base["Heading2"],
        textColor=colors.HexColor("#111827"),
        spaceBefore=10,
        spaceAfter=8,
    )

    return base, code, body, heading


def _analysis_paragraphs(analysis_text: str, body_style, heading_style):
    """Convert an analysis string (with ## headings) to a list of Flowables."""
    items = []
    for line in analysis_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            items.append(Paragraph(html.escape(line[3:]), heading_style))
        else:
            items.append(Paragraph(html.escape(line).replace("\n", "<br/>"), body_style))
    return items


def _make_doc(buffer: io.BytesIO, title: str) -> SimpleDocTemplate:
    return SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
        title=title,
    )


# ── Public renderers ──────────────────────────────────────────────────────────

def render_report_pdf(original_code: str, analysis_text: str, diagram_text: str) -> io.BytesIO:
    """Return a BytesIO PDF containing the original code, analysis, and diagrams."""
    buffer = io.BytesIO()
    doc = _make_doc(buffer, "AI Python Debugger Report")
    base, code_style, body_style, heading_style = _build_styles()

    story = [
        Paragraph("AI Python Debugger Report", base["Title"]),
        Spacer(1, 12),
        Paragraph("Original Buggy Code", heading_style),
        Preformatted(original_code, code_style),
        Paragraph("Analysis", heading_style),
        *_analysis_paragraphs(analysis_text, body_style, heading_style),
        Paragraph("Architecture Diagrams", heading_style),
        Preformatted(diagram_text or "No diagrams available.", code_style),
    ]

    doc.build(story)
    buffer.seek(0)
    return buffer


def render_engineering_note_pdf(
    original_code: str, analysis_text: str, diagram_text: str
) -> io.BytesIO:
    """Return a BytesIO PDF formatted as a formal engineering note."""
    buffer = io.BytesIO()
    doc = _make_doc(buffer, "Engineering Note: Python Debugging Review")
    base, code_style, body_style, heading_style = _build_styles()

    story = [
        Paragraph("Engineering Note: Python Debugging Review", base["Title"]),
        Spacer(1, 12),
        Paragraph("Fixed Code Context", heading_style),
        Preformatted(original_code, code_style),
        Paragraph("Engineering Summary", heading_style),
        *_analysis_paragraphs(analysis_text, body_style, heading_style),
        Paragraph("Behaviour Notes", heading_style),
        Preformatted(diagram_text or "No diagrams available.", code_style),
    ]

    doc.build(story)
    buffer.seek(0)
    return buffer
