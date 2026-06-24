# AI Python Debugger

> *Learn to Code, Code to Learn*

This project began after a **PyCon for Educators** session where **Dr. Oka** demonstrated a Python debugger extension he had built. Watching AI inspect code, explain bugs, and guide programmers through the debugging process was genuinely exciting, and I wanted to build my own version.

This repository is the result: an **AI-powered Python debugging assistant** that analyzes code, explains failures, suggests fixes, generates unit tests, writes engineering notes, and exports polished PDF reports.

I built the application in Python using **Panel** for the interface, **OpenRouter** as the model gateway, and **ReportLab** for report generation.

## Features

- **Code Editor:** Paste Python code directly into the browser.
- **AI Analysis:** Identify bugs, explain root causes, and generate fixed code.
- **Unit Test Suggestions:** Get test ideas for validating the fix.
- **ASCII Flow Diagrams:** Generate buggy and fixed execution flow charts.
- **Engineering Notes:** Export a formal technical note for the fix.
- **PDF Reports:** Download a professional report of the debugging session.
- **Follow-Up Questions:** Continue the conversation after the initial analysis.
- **Session Reset:** Start a fresh debugging session anytime.
- **Streaming Responses:** View model output as it arrives.

## Tech Stack

- **UI:** Panel
- **LLM Gateway:** OpenRouter via the OpenAI Python SDK
- **PDF Generation:** ReportLab
- **Environment Management:** python-dotenv

## Project Structure

```text
.
├── app.py             # Entry point: loads env, boots Panel, builds the UI
├── config.py          # Static prompts, model pool, and UI styles
├── llm_client.py      # OpenRouter client, fallback logic, and streaming helpers
├── state.py           # Session ID and per-session conversation history
├── note_generator.py  # Engineering note text generation
├── pdf_renderer.py    # PDF creation with ReportLab
├── ui.py              # Panel widgets, layout, and event handlers
├── requirements.txt
└── README.md
```

## Module Design

The codebase follows the **Single Responsibility Principle** so each module has one clear job.

- `app.py` loads environment variables, initializes Panel, imports the UI, and serves the app.
- `config.py` holds pure configuration with no side effects.
- `llm_client.py` owns all OpenRouter communication and streaming behavior.
- `state.py` manages session-scoped conversation history in Panel cache.
- `note_generator.py` builds the engineering note text by calling the LLM.
- `pdf_renderer.py` turns strings into PDF byte buffers.
- `ui.py` wires widgets, layout, and event handlers together.

This separation makes the app easier to test, safer to import, and simpler to extend.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/seanwhs/AI-Enabled-Python-Debugger.git
cd AI-Enabled-Python-Debugger
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure OpenRouter:

```env
OPENROUTER_API_KEY=your_api_key_here
```

5. Run the app:

```bash
panel serve app.py
```

Open `http://localhost:5006/app` in your browser.

## Live Deployment

You can try the app on Hugging Face in two ways:

- **Space page:** [https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger](https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger)
- **Direct app URL:** [https://seanwhs-ai-enabled-python-debugger.hf.space](https://seanwhs-ai-enabled-python-debugger.hf.space)

If the direct link appears blank, open the Space page first and wait for the app to wake up.

## What I Learned

Building this project was about more than calling an LLM API. I focused on:

- **State management:** keeping per-session conversation history in Panel cache.
- **Async responsiveness:** streaming responses without freezing the UI.
- **Reliable model access:** using OpenRouter with fallback models.
- **Document generation:** assembling structured PDFs programmatically.
- **Software design:** separating configuration, transport, state, UI, and rendering concerns.

## Future Improvements

- Upload `.py` files directly into the UI.
- Analyze multi-file projects.
- Add support for more languages such as JavaScript, Go, and C++.
- Add richer code diff presentation in the reports.
- Improve prompt-driven note formatting for more consistent engineering summaries.

## Acknowledgements

This project was inspired by **Dr. Oka** during the **PyCon for Educators** session. It reminded me that the best conference takeaways are often the projects you feel compelled to build afterward.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).