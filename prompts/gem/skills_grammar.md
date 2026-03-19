# Grammar skill

## Overview
This skill defines the structured process for generate documents for Greek grammar tutoring session.

---

## The Grammar Process

### 1. Grammar explanation
* **Grammar topic:** Keep the explanation of grammar topic that asked by user exactly for level that user asked.  
* **Format:** Keep the explanation in format from the reference `reference_grammar_explanation.md`.

### 2. Exercise Generation
* **Generate:** Generate the JSON file with the exercises according **Grammar Topic** that user provided. The content and the format see on **Exercises content:** and **JSON format:** below. Generate only **select** and **feel** types of exercises.   
* **Exercises content:** Pull description of exercises from the **Exercise Types** section of `reference_grammar_exercises.md`.
* **Translation:** Add translation of exercise like in `reference_exercise_example.json`.
* **JSON format:** JSON format should be like in example in `reference_exercise_example.json`.

---

## Prompt Examples
**For grammar explanation**
- "Using the grammar skill from the knowledge base, explain the grammar topic **Nouns** for level A1."
**For exercise generation**
- "Using the grammar skill from the knowledge base, generate the JSON file for grammar topic **Nouns**. Number of exercises: **5**."