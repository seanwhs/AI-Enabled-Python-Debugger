"""
llm_client.py
-------------
Owns everything that talks to the LLM:
  - OpenAI-compatible client initialisation
  - call_llm          – blocking or streaming, with model fallback
  - strip_fences      – post-processing utility for raw model output
  - stream_to_pane    – streams a response into a Panel pane in a background thread
  - generate_text     – single-shot (non-streaming) helper
"""

import os
import re
import threading
from typing import List, Dict

from openai import OpenAI
from tornado.iostream import StreamClosedError
from tornado.websocket import WebSocketClosedError

from config import MODELS_POOL


# ── Client singleton ──────────────────────────────────────────────────────────

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger",
        "X-Title": "AI Enabled Python Debugger",
    },
)


# ── Core LLM call with fallback ───────────────────────────────────────────────

def call_llm(messages: List[Dict], stream: bool = False):
    """Send *messages* to the first available model in MODELS_POOL."""
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


# ── Text utilities ────────────────────────────────────────────────────────────

def strip_fences(text: str) -> str:
    """Remove all triple-backtick fences from model output."""
    return re.sub(r"```[a-zA-Z0-9_-]*\n?", "", text).strip()


# ── Panel pane helpers ────────────────────────────────────────────────────────

def _safe_set(pane, text: str) -> bool:
    """Update *pane* safely; returns False when the browser has disconnected."""
    try:
        pane.object = text
        return True
    except (WebSocketClosedError, StreamClosedError):
        return False


def stream_to_pane(messages: List[Dict], pane, post_process=None) -> None:
    """
    Stream the model response into *pane* without blocking the UI thread.

    Parameters
    ----------
    messages     : Conversation history passed directly to call_llm.
    pane         : A Panel Markdown pane whose ``.object`` will be updated live.
    post_process : Optional ``str -> str`` applied once streaming finishes
                   (e.g. wrapping raw text in a code fence).
    """
    def _run():
        try:
            stream = call_llm(messages, stream=True)
        except Exception as e:
            _safe_set(pane, f"**Error:** {e}")
            return

        full = ""
        try:
            for chunk in stream:
                bit = getattr(chunk.choices[0].delta, "content", None)
                if not bit:
                    continue
                full += bit
                if not _safe_set(pane, full):
                    return
        except (WebSocketClosedError, StreamClosedError):
            return
        except Exception as e:
            _safe_set(pane, f"**Error:** {e}")
            return

        if post_process:
            full = post_process(full)
            _safe_set(pane, full)

        messages.append({"role": "assistant", "content": full})

    threading.Thread(target=_run, daemon=True).start()


def generate_text(messages: List[Dict]) -> str:
    """Return a complete (non-streaming) LLM response as a plain string."""
    resp = call_llm(messages, stream=False)
    return resp.choices[0].message.content or ""
