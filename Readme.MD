# AI Python Debugger

> *"Learn to Code, Code to Learn"*

I attended a **PyCon for Educators** session where **Dr. Oka** demonstrated a Python Debugger extension he had developed. Watching an AI inspect code, explain bugs, and guide programmers through the debugging process was genuinely exciting. By the time the session ended, I couldn't wait to try building one myself.

This project is the result.

Instead of creating a traditional debugger that steps through code line by line, I wanted to build an **AI-powered debugging assistant** that I could use to:

* explain *why* code fails,
* identify the root cause of bugs,
* suggest corrected code,
* recommend unit tests, and
* support follow-up questions through a conversational interface.

I built the entire application in Python using **Panel** for the interface and **OpenRouter** as the gateway to open-source language models.

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

### 💤 Troubleshooting: What if the direct link is blank? (The Wake-Up Trick 🪄)

When a Hugging Face Space goes to sleep after a period of inactivity, visiting my direct subdomain link (`.hf.space`) usually results in a blank page or a timeout error.

To wake up my Space completely on your own, I recommend simply poking Hugging Face's main gateway:

1. Visit my main dashboard link: [https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger](https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger)
2. **What happens behind the scenes:** Just by landing on this page, your browser sends a request to Hugging Face's servers saying, *"Hey, someone wants to look at this project."*
3. Hugging Face will immediately change the status badge at the top from **"Sleeping"** to **"Awaking"** or **"Running"**.
4. Once that status badge turns green and reads **"Running"** (which usually takes about 10–30 seconds), my direct link (`.hf.space`) will instantly work again.

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

If you would rather run this application locally on your machine, I have outlined the steps below:

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

* **Windows:** `.venv\Scripts\activate`
* **Linux / macOS:** `source .venv/bin/activate`

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

Then open your browser and go to: `http://localhost:5006/app`

---

# AI Prompt

I instruct the language model to return its analysis using a structured layout to keep every session consistent and easy for you to skim:

```markdown
## Error
## Explanation
## Fixed Code
## Unit Tests
## Improvements

```

---

# Conversation Memory

Unlike a single prompt-and-response application, my debugger maintains a complete conversational history. This allows you to ask immediate contextual questions such as:

> *"Why is this fix better?"* or *"Can you optimize it further?"*

without needing to re-paste your raw code file. If you want to clear your current history and start a fresh session, just hit the **Reset Conversation** button.

---

# Why OpenRouter?

I wanted this project to be inexpensive to run and easy for educators and students to experiment with. OpenRouter provides seamless access to multiple language models behind a single OpenAI-compatible API wrapper. This allows me to easily switch over to another free fallback model whenever a specific endpoint gets busy.

---

# What I Learned

Building this project taught me much more than simply calling an LLM API endpoint. I deeply explored:

* designing effective system prompts and guardrails,
* streaming AI responses natively in web applications,
* maintaining programmatic conversational state memory, and
* building interactive frontends using Panel.

It reinforced something I always emphasize to my students: **the fastest way to understand a new technology is to build something with it.**

---

# Future Improvements

I have several goals for the next version, including:

* Uploading `.py` files directly into the web UI,
* Multi-file project workspace analysis,
* Exportable/downloadable debugging PDF reports, and
* Support for additional programming languages (JavaScript, Go, C++).

---

# Acknowledgements

This project was inspired directly by a demonstration by **Dr. Oka** during our **PyCon for Educators** session. Sometimes the best conference takeaway isn't just a notebook full of conceptual ideas—it's the custom project repository you find yourself enthusiastically building that same evening.

---

# License

[MIT License](https://opensource.org/licenses/MIT)