# AI Python Debugger

> *"Learn to Code, Code to Learn"*

Today I attended a **PyCon for Educators** where **Dr. Oka** demonstrated a Python Debugger extension that he had developed. Watching an AI inspect code, explain bugs, and guide programmers through the debugging process was genuinely exciting. By the time the session ended, I couldn't wait to try building one myself.

This project is the result.

Instead of creating a traditional debugger that steps through code line by line, I wanted to build an **AI-powered debugging assistant** capable of:

* explaining *why* code fails,
* identifying the root cause of bugs,
* suggesting corrected code,
* recommending unit tests, and
* supporting follow-up questions through a conversational interface.

The entire application is built in Python using **Panel** for the interface and **OpenRouter** as the gateway to open-source language models.

---

# 🚀 Live Deployment on Hugging Face

You can access my app in your browser in two different ways, depending on whether you want to see the Hugging Face interface wrapper or view it as a completely clean, full-screen standalone application.

### 🌐 Option 1: The Standard Hugging Face Link (With Header)

This is my main Space homepage. It wraps my app inside the Hugging Face dashboard frame, allowing you to easily view my logs, files, or repository settings.

* **My Space URL:** [https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger](https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger)
* **How it works:** Once the status bar at the top changes from **Building** to a green **Running** badge, my Panel dashboard will load directly inside the page.

### 🖥️ Option 2: The Direct URL (Full-Screen & Branding-Free)

If you want to view my debugger as a regular, full-screen web application without any Hugging Face branding or menus around it, use this direct subdomain link:

* **Direct App URL:** [https://seanwhs-ai-enabled-python-debugger.hf.space](https://seanwhs-ai-enabled-python-debugger.hf.space)

> 💡 **Pro-Tip:** You can also find this direct link at any time from my main Space page by clicking the three vertical dots (**⋮**) in the top right corner, selecting **Embed this Space**, and copying the **Direct URL**.

---

# Features

* 🐍 Paste Python code into an editor
* 🤖 AI analyzes your code
* 🔍 Identifies bugs and explains root causes
* ✅ Generates corrected code
* 🧪 Suggests unit tests
* 💬 Supports follow-up questions while remembering previous context
* 🔄 Reset conversation for a fresh debugging session
* ⚡ Streaming responses for a more responsive experience
* 💸 Uses free models available through OpenRouter

---

# Example Workflow

```
Paste Python Code
        │
        ▼
Click "Debug Code"
        │
        ▼
AI analyzes the program
        │
        ├── Finds errors
        ├── Explains why
        ├── Fixes the code
        ├── Suggests tests
        └── Recommends improvements
        │
        ▼
Ask follow-up questions

```

---

# Tech Stack

* Python
* Panel
* OpenRouter API
* OpenAI Python SDK
* python-dotenv

---

# Project Structure

```
.
├── app.py
├── .env
├── requirements.txt
└── README.md

```

---

# Local Installation

If you would rather run this application locally on your machine, follow the steps below:

Clone my repository:

```bash
git clone https://github.com/seanwhs/AI-Enabled-Python-Debugger.git
cd AI-Enabled-Python-Debugger

```

Create a virtual environment:

```bash
python -m venv .venv

```

Activate it:

* **Windows:**
```bash
.venv\Scripts\activate

```


* **Linux / macOS:**
```bash
source .venv/bin/activate

```



Install the dependencies:

```bash
pip install -r requirements.txt

```

---

# Configure OpenRouter

Create a local `.env` file in the root folder:

```env
OPENROUTER_API_KEY=your_api_key_here

```

My application reads your API key automatically using **python-dotenv**.

---

# Running the Application Locally

Start the local Panel development server:

```bash
panel serve app.py --autoreload

```

Then open your browser and go to:

```text
http://localhost:5006/app

```

---

# AI Prompt

My debugger instructs the language model to return its analysis using the following structured layout. This keeps every debugging session completely consistent and easy for you to skim:

```markdown
## Error

## Explanation

## Fixed Code

## Unit Tests

## Improvements

```

---

# Conversation Memory

Unlike a single prompt-and-response application, my debugger maintains a complete conversational history.

This allows you to ask immediate contextual questions such as:

> Why is this fix better?

or

> Can you optimize it further?

without needing to re-paste your raw code file back into the editor. If you want to clear your current history and start a completely fresh debugging session, just hit the **Reset Conversation** button.

---

# Streaming Responses

Instead of forcing you to wait for the AI to finish generating its entire response block, my application streams individual tokens as they arrive from OpenRouter. This makes the interface feel highly interactive, fluid, and conversational.

---

# Why OpenRouter?

I wanted this project to be inexpensive to run and easy for educators and students to experiment with.

OpenRouter provides seamless access to multiple language models behind a single OpenAI-compatible API wrapper. This allows me to easily switch over to another free fallback model whenever a specific endpoint gets busy or goes offline. Changing our background model is as simple as updating one string literal:

```python
MODEL_NAME = "openrouter/free"

```

---

# What I Learned

Building this project taught me much more than simply calling an LLM API endpoint.

I deeply explored:

* designing effective system prompts and guardrails
* streaming AI responses natively in web applications
* maintaining programmatic conversational state memory
* building interactive frontends using Panel
* integrating OpenRouter with the official OpenAI SDK
* separating core application logic from frontend UI definitions
* using Python generators for incremental UI output streams
* managing state variables smoothly across sequential user actions

More importantly, it reinforced something I always emphasize to my students:

> The fastest way to understand a new technology is to build something with it.

---

# Future Improvements

Some ideas I'd love to implement next:

* Upload `.py` files directly into the web UI
* Multi-file project workspace analysis
* Robust syntax highlighting inside AI markdown outputs
* Exportable/downloadable debugging PDF reports
* Automatic test execution using a native `pytest` wrapper
* Static analysis checking with Ruff or Pylint integration
* Native Docker container configurations
* Interactive model selection toggles right on the UI layout
* Support for additional programming languages (JavaScript, Go, C++)
* Public GitHub repository link analysis

---

# Acknowledgements

This project was inspired directly by a demonstration by **Dr. Oka** during our **PyCon for Educators** session. Watching his AI-assisted debugger workflow in action motivated me to build out my own independent implementation the absolute moment I got back home.

Sometimes the best conference takeaway isn't just a notebook full of conceptual ideas—it's the custom project repository you find yourself enthusiastically building that same evening.

---

# License

[MIT License](https://www.google.com/search?q=LICENSE)