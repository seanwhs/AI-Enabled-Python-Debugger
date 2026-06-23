## 🧪 The Step-by-Step Testing Workflow

### Step 1: Initialize the Application

1. **Launch the Server**: Open your terminal in the directory containing `app.py` and run:
```bash
panel serve app.py --show

```


2. **Verify Launch**: Your browser should automatically open `http://localhost:5006/app`.
3. **Verify Configuration**: Check your terminal logs for the initialization debug line to confirm your `.env` is reading successfully:
> `DEBUG: API Key loaded: True`



---

### Step 2: The Core Debugging Test

1. **Input Code**: Paste this buggy snippet into the **Code Editor**:
```python
def get_pairwise_sums(numbers):
    sums = []
    for i in range(len(numbers)):
        current_sum = numbers[i] + numbers[i + 1]
        sums.append(current_sum)
    return sums
print(get_pairwise_sums([10, 20, 30, 40]))

```


2. **Execute**: Click the **⚡ Debug** button.
3. **Verify UI Flow**:
* The **Analysis** pane displays `_Analyzing…_`.
* The response streams chunk-by-chunk.


4. **Verify AI Agent Content**:
* **`## Error`**: Must identify the `IndexError` (off-by-one).
* **`## Explanation`**: Should explain that `numbers[i + 1]` attempts to access index `4` in a length `4` list during the final loop.
* **`## Fixed Code`**: Should suggest using `range(len(numbers) - 1)`.



---

### Step 3: The Diagram Generation Test

This validates your `on_diagram` handler and its integration with the `DIAGRAM_SYSTEM_PROMPT`.

1. **Execute**: Click the **📊 Diagram** button.
2. **Verify Output**: The app should stream two distinct ASCII flowcharts into the **Diagrams** pane, visualizing the logic flow before and after the fix.

---

### Step 4: The Chat History & Follow-Up Test

This validates your `on_followup` handler and ensures the conversation context is preserved.

1. **Input Question**: In the **Follow-Up** text field, type:
> *"Can you rewrite the fixed version using a list comprehension or zip instead of a traditional for loop?"*


2. **Execute**: Click **💬 Follow-Up**.
3. **Verify Context Retention**:
* The AI should acknowledge the previous context and provide:


```python
def get_pairwise_sums(numbers):
    return [a + b for a, b in zip(numbers, numbers[1:])]

```



---

### Step 5: The Clean Slate (Reset) Test

This ensures `on_reset` successfully wipes the `pn.state.cache` to prevent memory leakage between sessions.

1. **Execute**: Click the **🗑️ Reset** button.
2. **Verify UI Reset**: Both input fields and the output markdown panes should clear/revert to their placeholders.
3. **Verify Memory Wipe**: Ask a follow-up question such as: *"What code did I just ask you to fix?"*
4. **Expected Result**: Because the session cache was reset to the original `SYSTEM_PROMPT`, the AI should respond that it has no prior context, confirming the state is clean.