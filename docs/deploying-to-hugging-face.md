## Step 1: Create a New Hugging Face Space

1. Go to [Hugging Face](https://huggingface.co/) and log in.
2. Click on your profile picture in the top right and select **New Space**.
3. Fill out the details:
* **Space Name:** e.g., `AI-Enabled-Python-Debugger`
* **License:** (e.g., `mit` or `apache-2.0`)
* **Select the Space SDK:** Choose **Docker**.
* **Docker Template:** Choose **Blank**.
* **Space Visibility:** Public or Private (your choice).


4. Click **Create Space**.

---

## Step 2: Prepare Your Repository Files

You need to add two structural files alongside your `app.py` inside your repository: a `requirements.txt` and a `Dockerfile`.

### 1. `requirements.txt`

Create a file named `requirements.txt` and list your dependencies:

```text
panel
openai
python-dotenv

```

### 2. `Dockerfile`

Create a file named `Dockerfile` (no file extension). This tells Hugging Face how to install dependencies and spin up your Panel server:

```dockerfile
FROM python:3.11-slim

WORKDIR /code

# Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application
COPY . .

# Panel requires a specific port (7860) to work on Hugging Face Spaces
CMD ["panel", "serve", "app.py", "--address", "0.0.0.0", "--port", "7860", "--allow-websocket-origin=*"]

```

---

## Step 3: Configure Your API Key (Security)

> ⚠️ **CRITICAL:** Do **not** upload your `.env` file to Hugging Face. Committing your API keys publicly is dangerous.

Instead, use Hugging Face's built-in **Variables and Secrets** manager:

1. In your newly created Space, navigate to the **Settings** tab.
2. Scroll down to the **Variables and secrets** section.
3. Click **New secret**.
4. Set the name to `OPENROUTER_API_KEY` and paste your actual token into the value field.

*(Your `app.py` is already using `os.getenv("OPENROUTER_API_KEY")`, meaning it will automatically read this secret without any code changes!)*

---

## Step 4: Upload Your Files

You can upload your files (`app.py`, `requirements.txt`, and `Dockerfile`) in two ways:

### Option A: Directly on the Browser

1. In your Space, click the **Files** tab.
2. Click **Add file** -> **Upload files**.
3. Drag and drop your three files and commit them to the main branch.

### Option B: Via Git CLI

If you prefer terminal commands, clone the empty space repo locally and push your files:

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
# Move your app.py, requirements.txt, and Dockerfile into this directory
git add .
git commit -m "Deploy Panel AI debugger"
git push

```

---

## 🚀 What Happens Next?

Once the files are saved, Hugging Face will automatically detect the `Dockerfile` and begin building your application.

You can watch the build logs in real-time under the **App** tab. After 2–3 minutes, your interactive Python AI debugger UI will be live for anyone to use!

Don't panic! This is completely normal and **will not break your space permanently**.

Hugging Face Spaces automatically trigger a build container the exact second a new commit (like your `Dockerfile` or `app.py`) is pushed to the repository.

Here is what will happen and how to handle it:

### What to expect right now

Since the container is building without the `OPENROUTER_API_KEY` secret, the build itself will actually **succeed**, but when the app starts running, it will either throw an error in your UI or print `DEBUG: API Key loaded: False` in your logs and fail when you try to submit code.

### But I have not uploaded my API Keys!!!!

You do not need to delete the space or stop the build.

1. Go ahead and add your API key right now under **Settings** -> **Variables and secrets** -> **New secret** (Name it exactly `OPENROUTER_API_KEY`).
2. Once the secret is saved, scroll back up to the top of your Space page.
3. Click the **Factory Restart** button (located near the "App" and "Files" tabs, or inside the "Settings" menu).

A factory restart completely wipes the current running instance and boots up a brand-new container—this time instantly injecting the `OPENROUTER_API_KEY` environmental variable you just saved. Your app will be fully functioning within a couple of minutes!