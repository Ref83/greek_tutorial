# Roadmap skill

## Overview
This skill defines the structured process for generate roadmap steps.

---

## The Roadmap concepts

### 1. The Roadmap concept
* The roadmap consist of steps.
* The list of steps located in `content\roadmap\steps.json` file.
* The example of roadmap steps located in `roadmap_steps_example.json`.

### 2. Step content principle
* The step should consist of blocks that could be `grammar` or `vocabulary` type
* The `grammar` type represent one of the grammar topic
* The `vocabulary` type represent one of the vocabulary block.
* The list of grammar topics placed in `content\grammar\topics.json` file 
* The list of vocabulary topics the blocks placed in `content\vocabulary\topics.json` file and the block for topics placed in `content\vocabulary\{topic}\vocabulary.json` files 

### 3. Space repetition principle
* Each grammar topic as well as vocabulary block should be represented in roadmap steps many times according space repetition principles with intervals 1, 2, 5, 10, 20 steps.
* Each step should consist of 2 or 3 blocks
---

## Prompt Examples
- "Using the @prompts/gem/skills_radmap.md  skill, add 5 next steps"
