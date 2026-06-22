## 🧪 The Step-by-Step Testing Workflow

### Step 1: Initialize the Application

1. Open your terminal and start the Panel server:
```bash
panel serve app.py --show

```


2. Confirm the browser opens automatically to `http://localhost:5006/app`.
3. Check your terminal logs for the initialization debug line to confirm your `.env` is reading successfully:
> `DEBUG: API Key loaded: True`



---

### Step 2: The Core Debugging Test

1. **Input Code**: Copy and paste the buggy code block directly into the **Python Code** editor widget:
```python
def get_pairwise_sums(numbers):
    """Returns a list of sums of adjacent elements."""
    sums = []
    for i in range(len(numbers)):
        current_sum = numbers[i] + numbers[i + 1]
        sums.append(current_sum)
    return sums

print(get_pairwise_sums([10, 20, 30, 40]))

```


2. **Execute**: Click the **Debug Code** button.
3. **Verify App UI Behavior**:
* The Markdown window should immediately clear and display `Analyzing...`.
* Words should begin streaming dynamically into the **AI Analysis** window chunk-by-chunk.


4. **Verify AI Agent Content**:
Check if the LLM followed the `SYSTEM_PROMPT` rules. Ensure the output strictly includes these specific headers and expected answers:
* **`## Error`**: Should identify the `IndexError` (off-by-one error).
* **`## Explanation`**: Should explain that `numbers[i + 1]` attempts to read index `4` on a list of length `4` during the final iteration loop.
* **`## Fixed Code`**: Should suggest changing the loop to `range(len(numbers) - 1)`.
* **`## Unit Tests` & `## Improvements**`: Ensure these categories populate correctly.



---

### Step 3: The Chat History & Follow-Up Test

This steps tests your `on_followup` handler and ensures `conversation_messages` is correctly accumulating context.

1. **Input Question**: Locate the **Follow-Up-Question** text field at the bottom.
2. **Type the query**:
> *"Can you rewrite the fixed version using a list comprehension or zip instead of a traditional for loop?"*


3. **Execute**: Click the **Ask Follow-Up** button.
4. **Verify Behavior**:
* The app should stream a new reply appended/updated in the Markdown box.
* The LLM should successfully understand what "the fixed version" refers to because it remembers the prior user prompt and assistant response. It should give you something clean like:
```python
def get_pairwise_sums(numbers):
    return [a + b for a, b in zip(numbers, numbers[1:])]

```





---

### Step 4: The Clean Slate (Reset) Test

This checks whether your `on_reset` function correctly wipes the conversation state back to the original system instructions.

1. **Execute**: Click the **Reset Conversation** button.
2. **Verify Behavior**:
* The text input fields for both the code editor and the follow-up text boxes should completely clear out.
* The Markdown area should say: `"Conversation reset. Paste new code to start a fresh analysis."`


3. **State Verification**: Type a second follow-up question right away like: *"What code did I just ask you to fix?"*
4. **Expected Result**: Because the global `conversation_messages` list was reset to its initial `SYSTEM_PROMPT` state, the AI should have no memory of the pairwise sums function and respond stating it has no prior code context.