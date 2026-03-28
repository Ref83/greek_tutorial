# Content exercises page

The page should consist of 2 panels.
The top panel should show the statistic how many exercises used done and how many of it was with error.
On the top panel should be the button complete that leads to the previous page.
The main panel should show the current exercise.
The source of exercises is JSON files with names like `exercises*.json`
There could be many JSON files with exercises.
The exercises should be in random order from all available sources.
The page should show one exercise in a time.
When user completed exercise it should be able to go to the next by clicking the button "Next"
The type of exercise should be mentioned in the panel
The exercises should correspond to item by item_id 

## Type of exercises
Exercises could be the following types.

### Multiple Choice
**Goal:** Identify the correct vocabulary item among several options.

**View:**
- `header` should be on the panel
- Near the `header` should be the mark `?` and when user click it the `translations` should appear
- `options` should be in the panel
- When user check some options the script should check it with `answer` and if it is wrong - show the user correct answer with `explanation`

**Example**

Ο Γιώργος ___ στο σπίτι τώρα.

a) είναι  
b) είμαι  
c) είσαι  
d) είμαστε

**JSON format**
```json
{
    "id": "2d743b0d-027a-43aa-8781-c1312f1382b5",
    "item_id": "v1e1-001",
    "type": "select",
    "header": "Ο Γιώργος ___ στο σπίτι τώρα.",
    "translations": "Here translations of header to English",
    "options":
    {
        "a": "είναι",
        "b": "είμαι",
        "c": "είσαι",
        "d": "είμαστε"
    },
    "answer": "a",
    "explanation": "Explanation why a is correct answer"
}
```

### Fill in the Blank
**Goal:** Produce the correct vocabulary item.

**View:**
- `header` should be on the panel
- Near the `header` should be the mark `?` and when user click it the `translations` should appear
- The field for enter answer should be in the panel
- When user fill the answer and press the button the script should check it with `answer` and if it is wrong - show the user correct answer with `explanation`

**Example**

Εγώ ___ (write) ένα γράμμα.

**JSON format**
```json
{
    "id": "6e4c785b-c170-4d3a-914d-acac0e3cb9b4",
    "item_id": "v1e1-001",
    "type": "fill",
    "header": "___ (we are) στο σπίτι τώρα.",
    "translations": "Here translations of header to English",
    "answer": "είμαστε",
    "explanation": "Explanation why είμαστε is correct answer"
}
```

### Translate
**Goal:** Translate the phrase contains the vocabulary item.

**View:**
- `header` should be on the panel
- The field for enter answer should be in the panel
- When user fill the answer and press the button the script should check it with `answer` and if it is wrong - show the user correct answer with `explanation`

**Example**

Are you well today?

**JSON format**
```json
{
    "id": "e1a1-004",
    "item_id": "v1a1-001",
    "type": "translate",
    "header": "Are you well today?",
    "answer": "Εσύ είσαι καλά σήμερα;",
    "explanation": "The correct translation is Εσύ είσαι καλά σήμερα;."
}
```