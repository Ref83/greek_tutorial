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

### 3. Drill Exercise Generation

* **Generate:** Generate one or more JSON files named `content\vocabulary\<topic>\block_N_drill_K.json`, where N the number of block, K the number of file with exercises.
* **Scope:** Exercises must cover **only the vocabulary items** from `vocabulary.json` for the given block(s). No other words, sentences, or phrases.
* **Types per item:** For each vocabulary item generate exercises of all four drill types, ordered from easiest to hardest:
  1. `select` — given the Greek word, choose the correct English meaning from 4 options
  2. `blocks` — given the English meaning, assemble the Greek word from shuffled letter blocks
  3. `writing` — given the English meaning, type the Greek word from memory
  4. `gap` — given a Greek example sentence with the vocabulary item replaced by `___`, type the missing word
* **Blocks shuffling rule:** In a `blocks` exercise the `blocks` array must contain the individual characters of `answer` in **shuffled** (non-sequential) order so the learner cannot simply read them left-to-right.
* **Spaced-repetition ordering:** Interleave items using the interval sequence **1, 1, 3, 5, 7**. Start all items at their easiest type (`select`) and advance each item one difficulty level per appearance. The pattern ensures a word is seen again after 1 item, then 1, then 3, then 5, then 7 items apart. Example for word1, word2, word3:

  ```
  select-word1, select-word2, blocks-word1, select-word3, blocks-word2,
  writing-word1, blocks-word3, writing-word2, gap-word1, writing-word3,
  gap-word2, gap-word3
  ```

* **Options for `select`:** Provide 4 options (keys `a`–`d`). The correct answer must appear in a random position. Distractors should be meanings of other vocabulary items from the same block — never random unrelated words.
* **File size:** Split into multiple `drill_N.json` files if the total exercise count exceeds ~30 per file.
* **JSON format:** Follow the format defined in `reference_vocabulary_exercises.md` for each exercise type. Place all exercises under the top-level `"exercises"` array.

### 5. MP3 file for Story
* **Generate:** For each story generate mp3 file using script like `scripts\gen_story.py`.
* **Place:** Put the audio into `content\vocabulary\<topic>\story_block_N.mp3`, where N the number of block.

---

## Prompt Examples
**For vocabulary generation**
- "Using the vocabulary skill from the knowledge base, generate the JSON file for vocabulary for topic **Personal information** for level A1."
**For exercise generation**
- "Using the vocabulary skill from the knowledge base, generate the JSON file for vocabulary from file. Number of exercises for each item: **10**."