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

## Type of drill exercises

### Select
**Goal:** Given a Greek word, select the correct English translation from several options.

**View:**
- `header` shows the Greek word or phrase
- `options` shows English translation choices
- When user selects an option the script checks it against `answer` and shows correct answer if wrong

**Example**

καλά

a) today  
b) well  
c) you  
d) you are

**JSON format**
```json
{
    "id": "e1a1-005",
    "type": "select",
    "header": "καλά",
    "options": {
        "a": "today",
        "b": "well",
        "c": "you",
        "d": "you are"
    },
    "answer": "b"
}
```

### Blocks
**Goal:** Given an English translation, the user assembles the Greek word or phrase by selecting letter blocks in the correct order.

**View:**
- `header` shows the English translation
- A shuffled set of letter blocks is displayed
- The user taps/clicks blocks to build the Greek answer
- When all letters are placed the script checks the result and shows correct answer if wrong

**Example**

good

Blocks: [α] [λ] [κ] [α]

**JSON format**
```json
{
    "id": "e1a1-006",
    "type": "blocks",
    "header": "good",
    "answer": "καλά",
    "blocks": ["κ", "α", "λ", "ά"]
}
```

### Writing
**Goal:** Given an English translation, the user manually types the Greek word or phrase.

**View:**
- `header` shows the English translation
- A text input field is displayed for the user to type the Greek answer
- When the user submits, the script checks it against `answer` and shows the correct answer if wrong

**Example**

good

[text input]

**JSON format**
```json
{
    "id": "e1a1-007",
    "type": "writing",
    "header": "good",
    "answer": "καλά"
}
```

### Gap
**Goal:** Given a Greek sentence with the vocabulary item hidden, the user writes the missing word.

**View:**
- `header` shows the Greek sentence with `___` replacing the vocabulary item
- A text input field is displayed for the user to type the missing word
- When the user submits, the script checks it against `answer` and shows the correct answer if wrong

**Example**

Εσύ είσαι ___ σήμερα;

[text input]

**JSON format**
```json
{
    "id": "e1a1-008",
    "type": "gap",
    "header": "Εσύ είσαι ___ σήμερα;",
    "answer": "καλά"
}
```