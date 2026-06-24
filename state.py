"""
state.py
--------
Manages per-browser-session conversation history stored in Panel's cache.
No UI or LLM logic lives here.
"""

from typing import List, Dict

import panel as pn

from config import SYSTEM_PROMPT

SESSION_KEY     = "session_id"
DEFAULT_SESSION = "default"


def get_session_id() -> str:
    """Return the current browser session ID (falls back to DEFAULT_SESSION)."""
    return pn.state.session_args.get(SESSION_KEY, [DEFAULT_SESSION])[0]


def get_conversation() -> List[Dict[str, str]]:
    """
    Return the conversation history for the current session.
    Initialises a fresh history on first access.
    """
    sid = get_session_id()
    if sid not in pn.state.cache:
        pn.state.cache[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return pn.state.cache[sid]


def reset_conversation() -> None:
    """Discard the current conversation and start a fresh one."""
    sid = get_session_id()
    pn.state.cache[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
