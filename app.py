# app.py
import os  # Used to access environment variables

import panel as pn  # Framework for building the chat UI

from dotenv import load_dotenv  # Loads variables from a .env file
from openai import OpenAI  # Client library to interact with OpenRouter/OpenAI API

# Load Configuration from .env file
load_dotenv()

# Debug: check if the variable is loaded
print(f"DEBUG: API Key loaded: {os.getenv('OPENROUTER_API_KEY') is not None}")

# Initialize the Panel extension explicitly loading 'codeeditor' assets 
# to prevent WebSocket timeouts on headless hosting setups like Hugging Face
pn.extension('codeeditor')

# Agent Configuration: Define stable free models to iterate through if one fails
MODELS_POOL = [
    "openai/gpt-oss-20b:free",
    "cohere/north-mini-code:free",
    "meta-llama/llama-3.2-3b-instruct:free"
]

SYSTEM_PROMPT = """
You are an expert Python debugging assistant. 
Do not include your internal reasoning or chain-of-thought process in the final output 
unless requested.

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

# Initialize OpenRouter Client with explicit identification headers
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://huggingface.co/spaces/seanwhs/AI-Enabled-Python-Debugger",
        "X-Title": "AI Enabled Python Debugger"
    }
)

# Initialize conversation history with the system role to set the AI's persona
conversation_messages = [
    {
        'role': 'system', 
        'content': SYSTEM_PROMPT
    }
]

# Step 1. Write Logic
def debug_code_stream(code: str, instance: None = None):
    """
    Generator that yields chunks of the model's response as they arrive,
    while iterating through a fallback pool if rate limits are hit.
    """
    conversation_messages.append({'role': 'user', 'content': code})
    
    stream = None
    # Try each model in the pool sequentially if an error occurs (like a 429)
    for model in MODELS_POOL:
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=conversation_messages,
                max_tokens=2048,
                stream=True
            )
            break  # Successfully acquired a stream, break out of the loop
        except Exception as e:
            print(f"Model {model} failed with error: {e}. Trying next fallback...")
            continue
            
    if not stream:
        yield "⚠️ **Error:** All free OpenRouter endpoints are currently swamped or unavailable. Please try again in a few moments."
        return

    full_reply = ''
    # Process and yield chunks as they arrive from the working API connection
    for chunk in stream:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            full_reply += text
            yield text
            
    # Store the final full AI response in history to maintain context
    conversation_messages.append({'role': 'assistant', 'content': full_reply})

# Step 2. Create Widgets
code_input = pn.widgets.CodeEditor(
    name = 'Python Code',
    language = 'python',
    height = 350,
    sizing_mode = 'stretch_width',
)
    
debug_button = pn.widgets.Button(
    name = 'Debug Code',
    button_type = 'default',
)

followup_input = pn.widgets.TextInput(
    name = 'Follow-Up-Question',
    placeholder = 'Ask a question about the previous analysis...',
)

followup_button = pn.widgets.Button(
    name = 'Ask Follow-Up',
    button_type = 'light',
)

reset_button = pn.widgets.Button(
    name = 'Reset Conversation',
    button_type = 'danger',
)

output = pn.pane.Markdown(
    'AI Analysis:',
    height = 400,
)
    
# Step 3: Define Event Handlers (The "Glue" between logic and UI)
def on_click(event):
    code = code_input.value.strip()

    if not code:
        output.object = "Please enter some Python code."
        return

    output.object = "Analyzing...\n"

    try:
        full_text = ""
        for chunk in debug_code_stream(code, None):
            full_text += chunk
            output.object = full_text
    except Exception as e:
        output.object = f"Error: {e}"


def on_followup(event):
    question = followup_input.value.strip()

    if not question:
        output.object = "Please enter a follow-up question."
        return

    output.object = "Thinking about your follow-up...\n"

    try:
        full_text = ""
        for chunk in debug_code_stream(question, None):
            full_text += chunk
            output.object = full_text
    except Exception as e:
        output.object = f"Error: {e}"


def on_reset(event):
    global conversation_messages
    conversation_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]
    output.object = "Conversation reset. Paste new code to start a fresh analysis."
    followup_input.value = ""
    code_input.value = ""


debug_button.on_click(on_click)
followup_button.on_click(on_followup)
reset_button.on_click(on_reset)

# Step 4: Define Layout (Stack Components)
app = pn.Column(
"# AI Python Debugger",
code_input,
debug_button,
output,
"## Follow-up",
followup_input,
followup_button,
reset_button,
width=800,
)

# Step 5: Serve
app.servable()