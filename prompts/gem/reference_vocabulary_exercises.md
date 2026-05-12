# Greek Vocabulary Exercise Reference

This document describes the types of Greek vocabulary exercises that can be generated for practice and evaluation.

---

# Exercise Types

## Translation Exercise

**Goal:** Apply vocabulary in translation.

**Type** translate

**Example**

"We are reading a book."

**Student Response**

Διαβάζουμε ένα βιβλίο.

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