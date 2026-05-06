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
    `examples`: examples how usually this vocabulary item used.
    `collocations`: collocations of vocabulary items
* **Number of vocabulary items:** Generate exactly number of vocabulary items user asked. Divide those items into blocks by 10 - 15 items. DON'T provide sample with just couple of examples to ask user about content and format.
* **Story:** For each block generate a story with the vocabulary items from this block. Translate each sentence in the story. 
* **JSON Format:** Keep the format from the reference `reference_vocabulary_example.json` and place it into `content\vocabulary\<topic>\vocabulary.json`

### 2. Exercise Generation
* **Generate:** Generate the JSON file with the exercises for each block from `vocabulary.json` and name it `content\vocabulary\<topic>\block_N_exercises_K.json`, where N the number of block, K the number of file with exercises.  
* **Exercises content:** Pull description of exercises from the **Exercise Types** section of `reference_vocabulary_exercises.md`. You can use sentences from examples or story.
* **JSON format:** JSON format should be like in example in `reference_vocabulary_exercise_example.json`.

### 3. MP3 file for Story
* **Generate:** For each story generate mp3 file using script like `scripts\gen_story.py`. 
* **Generate:** Place the story into `content\vocabulary\<topic>\story_block_N.mp3`, where N the number of block.

---

## Prompt Examples
**For vocabulary generation**
- "Using the vocabulary skill from the knowledge base, generate the JSON file for vocabulary for topic **Personal information** for level A1."
**For exercise generation**
- "Using the vocabulary skill from the knowledge base, generate the JSON file for vocabulary from file. Number of exercises for each item: **10**."