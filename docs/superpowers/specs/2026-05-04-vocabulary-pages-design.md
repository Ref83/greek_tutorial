# Vocabulary Pages Design

**Date:** 2026-05-04
**Topic:** Four HTML pages for the vocabulary section of Greek Tutorial

---

## Overview

Four static HTML pages extending the existing vocabulary section. All pages live in `vocabulary/` and follow the established visual style (indigo accent `#4f46e5`, white cards, `#f5f5f0` background, 680px max-width). No back navigation — users rely on browser back button.

---

## Pages

### 1. `vocabulary/topic.html`

**URL params:** `?id={topicId}`

**Data source:** `../content/vocabulary/{topicId}/vocabulary.json`

**Behaviour:**
- Loads `vocabulary.json` and renders one clickable card per block in `blocks[]`.
- Each card label: `Block {N}. {K} items` (1-based block number, count of `items[]`).
- Clicking navigates to `block.html?id={topicId}&block={N}` where N is 0-based index.

---

### 2. `vocabulary/block.html`

**URL params:** `?id={topicId}&block={N}` (N = 0-based block index)

**Data source:** same `vocabulary.json`, reads `blocks[N]`

**Layout:**
- Top panel (white card): two buttons — `Exercises` and `Read`.
  - `Exercises` → `exercises.html?id={topicId}&block={N}`
  - `Read` → `read.html?id={topicId}&block={N}`
- Main list: one row per item showing the Greek `item` field.
- Clicking a row expands inline to reveal:
  - `meaning` (English)
  - `examples[]`: each as Greek `example` + `translation`
  - `collocations[]`: each as Greek `collocation` + `translation`
- Clicking an expanded row collapses it.

---

### 3. `vocabulary/exercises.html`

**URL params:** `?id={topicId}&block={N}` (N = 0-based block index)

**Data source:** `../content/vocabulary/{topicId}/block_{N+1}_exercises_1.json`, `block_{N+1}_exercises_2.json`, ... (fetch sequentially until 404)

**Layout:**
- Top panel: `{done} done / {errors} errors` stat label + `Complete` button (navigates back via `history.back()`).
- Main panel: one exercise at a time, exercise type label shown.
- All exercise JSONs are fetched, merged, and shuffled before starting.

**Translate exercise (`type: "translate"`):**
- Shows `header` as the prompt.
- Text input for the user's answer.
- Submit button: compares input to `answer` (case-insensitive, trimmed).
  - Correct: marks as done, shows `Next` button.
  - Wrong: shows correct `answer`, increments error count, shows `Next` button.
- `Next` button advances to the next exercise.
- After all exercises complete: shows a summary panel (`{done} done, {errors} errors`).

**Exercise discovery:**
- Fetch `block_{N+1}_exercises_1.json`, then `block_{N+1}_exercises_2.json`, etc. until a non-ok response. Merge all `exercises[]` arrays, then shuffle.

---

### 4. `vocabulary/read.html`

**URL params:** `?id={topicId}&block={N}` (N = 0-based block index)

**Data source:** `vocabulary.json` → `blocks[N].story.sentences[]`; audio: `../content/vocabulary/{topicId}/story_block_{N+1}.mp3`

**Layout:**
- Top panel: `Listen` button. Clicking plays the mp3 (toggle play/pause).
- Below: list of sentences from `story.sentences[]`.
  - Each row shows the Greek `sentence`.
  - Clicking toggles the `translation` inline below the sentence.

---

## Visual Style

Matches existing pages exactly:
- Font: system sans-serif (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`)
- Background: `#f5f5f0`
- Cards: `background: #fff`, `border-radius: 12px`, `box-shadow: 0 1px 4px rgba(0,0,0,0.08)`
- Accent: `#4f46e5` (indigo), light tint `#eef2ff`
- Max-width: `680px`, centered with `margin: 0 auto`
- Hover lift: `box-shadow: 0 4px 16px rgba(79,70,229,0.13)`, `transform: translateY(-2px)`

---

## File Structure

```
vocabulary/
  vocabulary.html   (existing — topic list)
  topic.html        (NEW — block list for a topic)
  block.html        (NEW — item list for a block)
  exercises.html    (NEW — exercise session)
  read.html         (NEW — story reader)
```

---

## Constraints

- Pure static HTML + vanilla JS, no build step.
- All data fetched via `fetch()` relative URLs — requires a local HTTP server (existing `run.sh`).
- No back navigation links — browser back button only.
- Exercise answer comparison: case-insensitive, trimmed whitespace.
