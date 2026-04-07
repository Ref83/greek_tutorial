# Vocabulary skill

## Overview
This skill defines the structured process for generate documents for Greek vocabulary tutoring session.

---

## The Vocabulary Process

### 1. Vocabulary Generation
* **Vocabulary topic:** Keep the vocabulary topic that asked by user exactly for level that user asked.  
* **Vocabulary content:**
  Generate the words and useful phrases corresponding the topic and instructions that user provides you.
  For each item provide: 
    `meaning`: meaning of item in English
    `forms`: gender for nouns and adjectives, conjugation in present tense for verbs.
    `usage_patterns`: patterns how usually this vocabulary item used.
    `collocations`: collocations of vocabulary items
    `additional_examples`: some examples of usages
    `notes`: some useful notes about the vocabulary item
* **Number of vocabulary items:** Generate exactly number of vocabulary items user asked. DON'T provide sample with just couple of examples to ask user about content and format.
* **JSON Format:** Keep the format from the reference `reference_vocabulary_example.json`.

### 2. Exercise Generation
* **Generate:** Generate the JSON file with the exercises according **Vocabulary Topic** that user provided. The content and the format see on **Exercises content:** and **JSON format:** below.   
* **Exercises content:** Pull description of exercises from the **Exercise Types** section of `reference_vocabulary_exercises.md`.
* **Item ID:**
  To generate exercises user should provide the vocabulary JSON file in format like `reference_vocabulary_example.json`.
  For each item from vocabulary generate number of exercises that user asked. 
  Mask exercises with `item_id` corresponding the item from vocabulary  
* **JSON format:** JSON format should be like in example in `reference_vocabulary_exercise_example.json`.

---

## Prompt Examples
**For vocabulary generation**
- "Using the vocabulary skill from the knowledge base, generate the JSON file for vocabulary for topic **Personal information** for level A1."
**For exercise generation**
- "Using the vocabulary skill from the knowledge base, generate the JSON file for vocabulary from file. Number of exercises for each item: **10**."