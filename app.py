"""
app.py
------
Entry point.  Loads environment variables, boots Panel, builds the UI,
and makes it servable.  No application logic lives here.

Run with:
    panel serve app.py
"""

from dotenv import load_dotenv
import panel as pn

load_dotenv()
pn.extension("codeeditor", sizing_mode="stretch_width", design="bootstrap")

from ui import build_ui  # noqa: E402 – import after pn.extension

app = build_ui()
app.servable()
