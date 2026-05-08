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
Generate **3 question sets** per text (matching the structure of the reference exams). For each question set:
* Provide a context-setting instruction in Greek (as in the exam format).
* State clearly how many answers are required (excluding the example).

Use the **Question Types** below, mixing at least 3 different types per exam:

#### Question Types

**Type 1 — True / False (ΣΩΣΤΟ / ΛΑΘΟΣ)**
* Generate 7 statements about the text. Exactly one is the solved example.
* Mix correct and incorrect statements. Incorrect ones should contain plausible errors (wrong number, wrong place, negated fact).
* Format: numbered table with ΣΩΣΤΟ | ΛΑΘΟΣ columns.

**Type 2 — Sentence Completion Matching (two-column)**
* Table A: 6 sentence beginnings derived from the text.
* Table B: 8–9 sentence endings (6 correct + 2–3 distractors that don't match any beginning).
* Student matches each beginning to the correct ending by number.
* Format: two side-by-side numbered lists.

**Type 3 — Multiple Choice (a / b / c)**
* Generate 4 questions, each with 3 options.
* Only one option is correct; distractors must be plausible (slightly wrong quantity, similar but different adjective, opposite direction, etc.).

### 4. JSON Output
* Save the caption and level in `content/reading/items.json`
* Save the full exercise as a JSON file at `content/reading/{id}/reading_<N>.json`, where N is the exercise number, and id is id of item in `content/reading/items.json`   
* JSON format: follow the structure below.

Example of `content/reading/items.json`
```json
{
  "items": [
    {
      "id": "a1_about_myself",
      "level": "a1",
      "cation": "About myself"
    },
    {
      "id": "a1_in_the_shop",
      "level": "a1",
      "cation": "In the shop"
    }
  ]  
}
```

Example of `content/reading/{id}/reading_<N>.json` 
```json
{
  "text": {
    "greek": "...",
    "english": "..."
  },
  "questions": [
    {
      "type": "true_false",
      "statement": "...", 
      "answer": "true"
    },
    {
      "type": "matching",
      "beginnings": [
        { "text": "..." }
      ],
      "endings": [
        { "text": "..." },
        { "text": "..." }
      ],
      "answers": { "0": 3, "1": 7 }
    },
    {
      "type": "multiple_choice",
      "question": "...",
      "options": { "a": "...", "b": "...", "c": "..." },
      "answer": "b"
    }
  ]
}
```

---

## Prompt Examples
- "Using the reading skill from the knowledge base, generate a reading exercise for level **A1** on the topic **personal introduction**."
