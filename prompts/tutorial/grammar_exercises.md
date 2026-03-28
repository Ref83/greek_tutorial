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

## Type of exercises
Exercises could be the following types. 

### Multiple Choice
**Goal:** Identify the correct grammatical form among several options.

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
**Goal:** Produce the correct grammatical form.

**View:**
- `header` should be on the panel
- Near the `header` should be the mark `?` and when user click it the `translations` should appear
- Tee field for enter answer should be in the panel
- When user fill the answer and press the button the script should check it with `answer` and if it is wrong - show the user correct answer with `explanation`

**Example**

Εγώ ___ (γράφω) ένα γράμμα.

**JSON format**
```json
{
    "id": "6e4c785b-c170-4d3a-914d-acac0e3cb9b4",
    "type": "fill",
    "header": "___ στο σπίτι τώρα.",
    "translations": "Here translations of header to English",
    "answer": "είμαστε",
    "explanation": "Explanation why είμαστε is correct answer"
}
```

## Matching Exercise

**Goal:**  
Match related items from two columns (e.g. verbs with conjugations).

---

### View

- Two columns should be displayed:
    - Left column (`left_items`)
    - Right column (`right_items`)
- Each column contains 4 (or more) items
- The user should be able to select or drag to match pairs between left and right
- The exercises is completed when the user match all the items

### Example

**Left:**
1. εγώ
2. εσύ
3. αυτός/αυτή/αυτό
4. εμείς

**Right:**
1. είναι  
2. είμαι  
3. είμαστε  
4. είσαι

---

### JSON format

```json
{
    "id": "9f1c2a77-3c4e-4c2b-9c1a-123456789abc",
    "type": "match",
    "left_items": {
        "1": "εσύ",
        "2": "εσύ",
        "3": "αυτός/αυτή/αυτό",
        "4": "εμείς"
    },
    "right_items": {
        "1": "είναι",
        "2": "είμαι",
        "3": "είμαστε",
        "4": "είσαι"
    },
    "answer": {
        "1": "2",
        "2": "4",
        "3": "1",
        "4": "3"
    }
}
```