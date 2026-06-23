# AI Python Debugger

> *"Learn to Code, Code to Learn"*

I attended a **PyCon for Educators** session where **Dr. Oka** demonstrated a Python Debugger extension he had developed. Watching an AI inspect code, explain bugs, and guide programmers through the debugging process was genuinely exciting. By the time the session ended, I couldn't wait to try building one myself.

This project is the result.

Instead of creating a traditional debugger that steps through code line by line, I built an **AI-powered debugging assistant** that I can use to:

* Explain *why* code fails,
* Identify the root cause of bugs,
* Provide fixed code,
* Generate unit tests,
* Create technical documentation, and
* Export findings as professional PDFs.

I built the entire application in Python using **Panel** for the interface, **OpenRouter** as the gateway to open-source language models, and **ReportLab** for report generation.

---

# 🚀 Live Deployment on Hugging Face

You can access my app in your browser in two different ways:

### 🌐 Option 1: The Standard Hugging Face Link (With Header)

This is my main Space homepage. It wraps my app inside the Hugging Face dashboard frame, allowing you to easily view my logs, files, or repository settings.

* **My Space URL:** [https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger](https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger)

### 🖥️ Option 2: The Direct URL (Full-Screen & Branding-Free)

If you want to view my debugger as a regular, full-screen web application without any Hugging Face branding or menus around it, use this direct subdomain link:

* **Direct App URL:** [https://seanwhs-ai-enabled-python-debugger.hf.space](https://seanwhs-ai-enabled-python-debugger.hf.space)

> 💡 **Troubleshooting:** If the page appears blank, visit the main Space URL first. Hugging Face might be waking the app from sleep mode. Once the status badge turns green, the direct link will work perfectly.

---

# Features

* 🐍 **Code Editor:** Paste Python code directly into the browser.
* 🤖 **AI Analysis:** Identifies bugs, explains causes, and provides fixes.
* 📊 **Architecture Visualization:** Generates ASCII flow charts for both buggy and fixed code.
* 🧾 **Professional Documentation:** * **Download Report:** A complete PDF summary of your debugging session.
* **Engineering Note:** A specialized, formal technical postmortem PDF for your fixes.


* 💬 **Conversational Memory:** Remembers context for follow-up questions.
* 🔄 **Reset Session:** Easily start a fresh debugging session.
* ⚡ **Streaming Responses:** Real-time text generation for a responsive experience.

---

# Tech Stack

* **Framework:** Panel
* **LLM Integration:** OpenAI Python SDK (via OpenRouter)
* **PDF Generation:** ReportLab
* **Environment Management:** python-dotenv

---

# Project Structure

```text
.
├── app.py           # Main application logic and UI
├── .env             # API key storage
├── requirements.txt # Dependencies
└── README.md

```

---

# Installation & Local Setup

If you want to run this application on your local machine:

1. **Clone the repository:**
```bash
git clone https://github.com/seanwhs/AI-Enabled-Python-Debugger.git
cd AI-Enabled-Python-Debugger

```


2. **Setup virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure OpenRouter:**
Create a `.env` file in the root folder and add your key:
```env
OPENROUTER_API_KEY=your_api_key_here

```


5. **Run the app:**
```bash
panel serve app.py --autoreload

```


Open `http://localhost:5006/app` in your browser.

---

# What I Learned

Building this project taught me much more than simply calling an LLM API. I focused on:

* **State Management:** Maintaining conversation memory across different users using `pn.state.cache`.
* **Asynchronous UI:** Using `threading` to keep the UI responsive while streaming AI tokens.
* **PDF Generation:** Programmatically building layout-intensive technical reports.
* **Robustness:** Implementing resilient API calls with automatic model failover via the OpenRouter pool.

---

# Future Improvements

* Uploading `.py` files directly into the UI.
* Multi-file project workspace analysis.
* Support for additional programming languages (JavaScript, Go, C++).

---

# Acknowledgements

This project was inspired directly by a demonstration by **Dr. Oka** during our **PyCon for Educators** session. It is a reminder that the best conference takeaways are the custom projects you feel inspired to build yourself.

---

# License

[MIT License](https://opensource.org/licenses/MIT)