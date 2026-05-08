# Reading skill

## Overview
This skill defines the structured process for generating reading comprehension exercises for Greek tutoring sessions, following the format of official Greek language proficiency certification exams (ΠΙΣΤΟΠΟΙΗΣΗ ΕΠΑΡΚΕΙΑΣ ΤΗΣ ΕΛΛΗΝΟΜΑΘΕΙΑΣ — ΚΑΤΑΝΟΗΣΗ ΓΡΑΠΤΟΥ ΛΟΓΟΥ).

---

## Text Types by Level

| Level | Text types | Word count |
|-------|-----------|------------|
| A1 | Invitations, profile cards, short personal letters, simple directions with visuals | 50–100 words |
| A2 | Announcements, ads, short articles, postcards, simple forms | 80–150 words |
| B1 | News items, blog posts, longer letters, brochures, short interviews | 150–250 words |

---

## The Reading Process

### 1. Text Generation
* **Topic:** Keep the topic and level that the user requests. Choose a realistic, everyday context (e.g. a christening invitation, a personal profile, a letter about a house, travel directions).
* **Language:** Write the text in Modern Greek appropriate to the level. Use only vocabulary and grammar structures expected at that level.
* **Authenticity:** Format the text realistically — a real invitation card, a letter with greeting/closing, a social-media profile table, etc.
* **Translation:** Provide a full English translation of the generated text immediately after the Greek original.

### 2. Question Generation
Generate **4 question sets** per text (matching the structure of the reference exams). For each question set:
* Provide a context-setting instruction in Greek (as in the exam format).
* Include one solved example item (ΠΑΡΑΔΕΙΓΜΑ / item 0) with the answer already given.
* State clearly how many answers are required (excluding the example).

Use the **Question Types** below, mixing at least 3 different types per exam:

#### Question Types

**Type 1 — True / False (ΣΩΣΤΟ / ΛΑΘΟΣ)**
* Generate 7 statements about the text. Exactly one is the solved example.
* Mix correct and incorrect statements. Incorrect ones should contain plausible errors (wrong number, wrong place, negated fact).
* Format: numbered table with ΣΩΣΤΟ | ΛΑΘΟΣ columns.

**Type 2 — Sentence Completion Matching (two-column)**
* Table A: 6 sentence beginnings derived from the text (plus 1 example).
* Table B: 8–9 sentence endings (6 correct + 2–3 distractors that don't match any beginning).
* Student matches each beginning to the correct ending by number.
* Format: two side-by-side numbered lists.

**Type 3 — Multiple Choice (α / β / γ)**
* Generate 4 questions (plus 1 example), each with 3 options.
* Only one option is correct; distractors must be plausible (slightly wrong quantity, similar but different adjective, opposite direction, etc.).
* Format: numbered blocks, each with α / β / γ options and a checkbox column.

**Type 4 — Visual / Blank Matching**
* Provide a short text with 4 blanks (plus 1 example blank already filled).
* Provide 6 numbered image descriptions or short phrases; 4 match the blanks, 2 are distractors.
* Format: text with underlined blanks and a numbered image/phrase list beside it.

### 3. Answer Key
* After all question sets, output a complete answer key section (ΛΥΣΕΙΣ) with every correct answer indicated, reproducing the question tables with answers filled in.

### 4. JSON Output
* Save the full exercise as a JSON file at `content/reading/<topic>/<level>_reading_<N>.json`, where N is the exercise number.
* JSON format: follow the structure below.

```json
{
  "level": "A1",
  "topic": "Christening invitation",
  "text": {
    "greek": "...",
    "english": "..."
  },
  "questions": [
    {
      "id": 1,
      "type": "true_false",
      "instruction": "Διαβάστε το κείμενο και σημειώστε ΣΩΣΤΟ ή ΛΑΘΟΣ.",
      "points": 7,
      "example": {
        "id": 0,
        "statement": "...",
        "answer": "ΣΩΣΤΟ"
      },
      "items": [
        { "id": 1, "statement": "...", "answer": "ΣΩΣΤΟ" },
        { "id": 2, "statement": "...", "answer": "ΛΑΘΟΣ" }
      ]
    },
    {
      "id": 2,
      "type": "matching",
      "instruction": "Βρείτε τη σωστή συνέχεια των φράσεων.",
      "points": 6,
      "example": { "id": 0, "beginning": "...", "ending_id": 5, "ending": "..." },
      "beginnings": [
        { "id": 1, "text": "..." }
      ],
      "endings": [
        { "id": 1, "text": "..." },
        { "id": 2, "text": "..." }
      ],
      "answers": { "1": 3, "2": 7 }
    },
    {
      "id": 3,
      "type": "multiple_choice",
      "instruction": "Διαβάστε και σημειώστε τη σωστή απάντηση.",
      "points": 6,
      "example": {
        "id": 0,
        "question": "...",
        "options": { "α": "...", "β": "...", "γ": "..." },
        "answer": "γ"
      },
      "items": [
        {
          "id": 1,
          "question": "...",
          "options": { "α": "...", "β": "...", "γ": "..." },
          "answer": "β"
        }
      ]
    },
    {
      "id": 4,
      "type": "visual_matching",
      "instruction": "Σημειώστε στα κενά τον αριθμό της σωστής εικόνας.",
      "points": 6,
      "text_with_blanks": "... [0_EXAMPLE] ... [1] ... [2] ... [3] ... [4] ...",
      "example_answer": 0,
      "options": [
        { "id": 0, "description": "highway / open road" },
        { "id": 1, "description": "left-turn sign" },
        { "id": 2, "description": "right-turn sign" },
        { "id": 3, "description": "STOP sign" },
        { "id": 4, "description": "house / building" },
        { "id": 5, "description": "traffic light (red)" },
        { "id": 6, "description": "railway tracks" }
      ],
      "answers": { "1": 5, "2": 2, "3": 1, "4": 4 }
    }
  ]
}
```

---

## Prompt Examples

**For reading text + exercises:**
- "Using the reading skill from the knowledge base, generate a reading exercise for level **A1** on the topic **personal introduction**. Include all 4 question types and the answer key."

**For a specific question type only:**
- "Using the reading skill from the knowledge base, generate a **True/False** question set for level **A2** based on the following text: [paste text]."

**For JSON file generation:**
- "Using the reading skill from the knowledge base, generate the JSON file for reading exercise **1** for level **A1**, topic **house description**."
