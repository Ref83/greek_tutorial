# Vocabulary exercises page

The page should consist of 2 panels.
The top panel should show the statistic how many exercises used done and how many of it was with error.
On the top panel should be the button complete that leads to the previous page.
The main panel should show the current exercise.
The source of exercises is JSON files with names like `block_<N>_exercises*.json`, where the N corresponds to the block number
There could be many JSON files with exercises.
The exercises should be in random order from all available sources.
The page should show one exercise in a time.
When user completed exercise it should be able to go to the next by clicking the button "Next"
The type of exercise should be mentioned in the panel
The exercises should correspond to item by item_id 

## Type of exercises
Exercises could be the following types.

### Translate
**Goal:** Translate the phrase contains the vocabulary item.

**View:**
- `header` should be on the panel
- The field for enter answer should be in the panel
- When user fill the answer and press the button the script should check it with `answer` and if it is wrong - show the user correct `answer`

**Example**

Are you well today?

**JSON format**
```json
{
    "id": "e1a1-004",
    "type": "translate",
    "header": "Are you well today?",
    "answer": "Εσύ είσαι καλά σήμερα;"
}
```