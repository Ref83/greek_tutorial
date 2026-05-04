# Vocabulary Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create four static HTML pages — `topic.html`, `block.html`, `exercises.html`, `read.html` — in `vocabulary/` to implement the vocabulary section flow.

**Architecture:** Pure static HTML + vanilla JS, no build step. Data loaded via `fetch()` from JSON files under `content/vocabulary/`. Pages chain via URL query params `?id={topicId}&block={N}` (block is 0-based index). Existing `vocabulary/vocabulary.html` already links to `topic.html?id=...`.

**Tech Stack:** HTML5, vanilla JS (ES6+), CSS3. Served via local HTTP server (`run.sh`).

---

## File Structure

| File | Action | Responsibility |
|---|---|---|
| `vocabulary/topic.html` | Create | List blocks for a topic; links to block.html |
| `vocabulary/block.html` | Create | List vocabulary items with expand/collapse; top nav to exercises/read |
| `vocabulary/exercises.html` | Create | Exercise session: fetch+shuffle JSON files, track stats, check answers |
| `vocabulary/read.html` | Create | Story reader with click-to-reveal translations and audio playback |

---

## Task 1: `vocabulary/topic.html`

**Files:**
- Create: `vocabulary/topic.html`

- [ ] **Step 1: Create the file with full implementation**

Create `vocabulary/topic.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vocabulary Topic – Greek Tutorial</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f0;
            color: #1a1a1a;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .page-header {
            max-width: 680px;
            margin: 0 auto 36px;
        }
        h1 {
            font-size: 1.6rem;
            font-weight: 600;
            color: #333;
            letter-spacing: 0.02em;
        }
        .blocks-list {
            max-width: 680px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .block-card {
            background: #fff;
            border-radius: 12px;
            padding: 20px 28px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            text-decoration: none;
            color: #1a1a1a;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: box-shadow 0.18s, transform 0.18s;
        }
        .block-card:hover {
            box-shadow: 0 4px 16px rgba(79,70,229,0.13);
            transform: translateY(-2px);
        }
        .block-name {
            font-size: 1rem;
            font-weight: 500;
        }
        .block-arrow {
            color: #4f46e5;
            font-size: 1.1rem;
        }
        @media (max-width: 480px) {
            h1 { font-size: 1.3rem; }
            .block-card { padding: 18px 20px; }
        }
    </style>
</head>
<body>
    <div class="page-header">
        <h1 id="topicTitle">Loading...</h1>
    </div>
    <div class="blocks-list" id="blocksList"></div>
    <script>
        const params = new URLSearchParams(window.location.search);
        const topicId = params.get('id');
        const blocksList = document.getElementById('blocksList');

        Promise.all([
            fetch('../content/vocabulary/topics.json').then(r => r.json()),
            fetch(`../content/vocabulary/${topicId}/vocabulary.json`).then(r => {
                if (!r.ok) throw new Error('Not found');
                return r.json();
            })
        ]).then(([topicsData, vocabData]) => {
            const topic = (topicsData.topics || []).find(t => t.id === topicId);
            if (topic) {
                document.title = topic.name + ' – Greek Tutorial';
                document.getElementById('topicTitle').textContent = topic.name;
            }

            const blocks = vocabData.blocks || [];
            if (!blocks.length) {
                blocksList.innerHTML = '<div class="block-card"><span class="block-name">No blocks available.</span></div>';
                return;
            }

            blocks.forEach((block, i) => {
                const a = document.createElement('a');
                a.className = 'block-card';
                a.href = `block.html?id=${encodeURIComponent(topicId)}&block=${i}`;
                a.innerHTML = `<span class="block-name">Block ${i + 1}. ${(block.items || []).length} items</span><span class="block-arrow">→</span>`;
                blocksList.appendChild(a);
            });
        }).catch(() => {
            blocksList.innerHTML = '<div class="block-card"><span class="block-name">Unable to load vocabulary.</span></div>';
        });
    </script>
</body>
</html>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8000/vocabulary/topic.html?id=personal_information` (or whichever port `run.sh` uses).

Expected:
- Page title shows the topic name (e.g., "Personal Information")
- Two block cards appear: "Block 1. 2 items" and "Block 2. 2 items"
- Clicking a card navigates to `block.html?id=personal_information&block=0`
- Hover shows lift shadow

- [ ] **Step 3: Commit**

```bash
git add vocabulary/topic.html
git commit -m "feat: add vocabulary topic page with block list"
```

---

## Task 2: `vocabulary/block.html`

**Files:**
- Create: `vocabulary/block.html`

- [ ] **Step 1: Create the file with full implementation**

Create `vocabulary/block.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vocabulary Block – Greek Tutorial</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f0;
            color: #1a1a1a;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .top-panel {
            max-width: 680px;
            margin: 0 auto 20px;
            background: #fff;
            border-radius: 12px;
            padding: 16px 28px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            display: flex;
            gap: 12px;
        }
        .action-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 8px;
            transition: background 0.15s;
        }
        .exercises-btn { color: #4f46e5; background: #eef2ff; }
        .exercises-btn:hover { background: #e0e7ff; }
        .read-btn { color: #059669; background: #ecfdf5; }
        .read-btn:hover { background: #d1fae5; }
        .items-list {
            max-width: 680px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .item-row {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        .item-header {
            padding: 18px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            user-select: none;
        }
        .item-header:hover { background: #f8f7ff; }
        .item-greek {
            font-size: 1rem;
            font-weight: 600;
            color: #1a1a1a;
        }
        .item-toggle {
            color: #4f46e5;
            font-size: 1.1rem;
            transition: transform 0.2s;
        }
        .item-row.open .item-toggle { transform: rotate(90deg); }
        .item-detail {
            display: none;
            padding: 0 28px 20px;
            border-top: 1px solid #f0f0f0;
        }
        .item-row.open .item-detail { display: block; }
        .detail-meaning {
            font-size: 0.95rem;
            color: #555;
            margin: 14px 0 16px;
        }
        .detail-section-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #9ca3af;
            margin-bottom: 8px;
        }
        .detail-examples, .detail-collocations {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 16px;
        }
        .detail-entry {
            background: #f8f7ff;
            border-radius: 8px;
            padding: 10px 14px;
        }
        .detail-greek { font-size: 0.95rem; color: #1a1a1a; margin-bottom: 2px; }
        .detail-translation { font-size: 0.85rem; color: #888; }
        @media (max-width: 480px) {
            .item-header { padding: 16px 20px; }
            .item-detail { padding: 0 20px 16px; }
            .top-panel { padding: 14px 20px; }
        }
    </style>
</head>
<body>
    <div class="top-panel">
        <a class="action-btn exercises-btn" id="exercisesBtn" href="#">✏️ Exercises</a>
        <a class="action-btn read-btn" id="readBtn" href="#">📖 Read</a>
    </div>
    <div class="items-list" id="itemsList"></div>
    <script>
        const params = new URLSearchParams(window.location.search);
        const topicId = params.get('id');
        const blockIndex = parseInt(params.get('block') || '0', 10);

        document.getElementById('exercisesBtn').href =
            `exercises.html?id=${encodeURIComponent(topicId)}&block=${blockIndex}`;
        document.getElementById('readBtn').href =
            `read.html?id=${encodeURIComponent(topicId)}&block=${blockIndex}`;

        fetch(`../content/vocabulary/${topicId}/vocabulary.json`)
            .then(r => { if (!r.ok) throw new Error(); return r.json(); })
            .then(data => {
                const block = (data.blocks || [])[blockIndex];
                if (!block) return;
                document.title = `Block ${blockIndex + 1} – Greek Tutorial`;

                const list = document.getElementById('itemsList');
                (block.items || []).forEach(item => {
                    const examplesHtml = (item.examples || []).map(e => `
                        <div class="detail-entry">
                            <div class="detail-greek">${e.example}</div>
                            <div class="detail-translation">${e.translation}</div>
                        </div>`).join('');

                    const collocationsHtml = (item.collocations || []).map(c => `
                        <div class="detail-entry">
                            <div class="detail-greek">${c.collocation}</div>
                            <div class="detail-translation">${c.translation}</div>
                        </div>`).join('');

                    const row = document.createElement('div');
                    row.className = 'item-row';
                    row.innerHTML = `
                        <div class="item-header">
                            <span class="item-greek">${item.item}</span>
                            <span class="item-toggle">›</span>
                        </div>
                        <div class="item-detail">
                            <div class="detail-meaning">${item.meaning}</div>
                            ${examplesHtml ? `<div class="detail-section-label">Examples</div><div class="detail-examples">${examplesHtml}</div>` : ''}
                            ${collocationsHtml ? `<div class="detail-section-label">Collocations</div><div class="detail-collocations">${collocationsHtml}</div>` : ''}
                        </div>`;

                    row.querySelector('.item-header').addEventListener('click', () => {
                        row.classList.toggle('open');
                    });
                    list.appendChild(row);
                });
            });
    </script>
</body>
</html>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8000/vocabulary/block.html?id=personal_information&block=0`

Expected:
- Top panel shows "✏️ Exercises" (indigo) and "📖 Read" (green) buttons
- Items listed — clicking a row expands to show meaning, examples, collocations
- Clicking an expanded row collapses it
- Exercises button navigates to `exercises.html?id=personal_information&block=0`
- Read button navigates to `read.html?id=personal_information&block=0`

- [ ] **Step 3: Commit**

```bash
git add vocabulary/block.html
git commit -m "feat: add vocabulary block page with expandable items"
```

---

## Task 3: `vocabulary/exercises.html`

**Files:**
- Create: `vocabulary/exercises.html`

- [ ] **Step 1: Create the file with full implementation**

Create `vocabulary/exercises.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exercises – Greek Tutorial</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f0;
            color: #1a1a1a;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .stats-panel {
            max-width: 680px;
            margin: 0 auto 20px;
            background: #fff;
            border-radius: 12px;
            padding: 16px 28px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .stats-text {
            font-size: 0.95rem;
            color: #555;
            font-weight: 500;
        }
        .stats-text .errors { color: #dc2626; font-weight: 700; }
        .complete-btn {
            padding: 8px 18px;
            border-radius: 8px;
            border: none;
            background: #eef2ff;
            color: #4f46e5;
            font-size: 0.9rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: background 0.15s;
        }
        .complete-btn:hover { background: #e0e7ff; }
        .exercise-panel {
            max-width: 680px;
            margin: 0 auto;
            background: #fff;
            border-radius: 12px;
            padding: 32px 36px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        }
        .exercise-type {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #9ca3af;
            margin-bottom: 16px;
        }
        .exercise-header {
            font-size: 1.15rem;
            font-weight: 600;
            color: #111;
            margin-bottom: 24px;
            line-height: 1.5;
        }
        .answer-input {
            width: 100%;
            padding: 12px 16px;
            border: 1.5px solid #d1d5db;
            border-radius: 8px;
            font-size: 1rem;
            font-family: inherit;
            color: #1a1a1a;
            outline: none;
            transition: border-color 0.15s;
        }
        .answer-input:focus { border-color: #4f46e5; }
        .answer-input.correct { border-color: #059669; background: #f0fdf4; }
        .answer-input.wrong { border-color: #dc2626; background: #fef2f2; }
        .answer-input:disabled { background: #f9fafb; cursor: default; }
        .feedback {
            margin-top: 12px;
            font-size: 0.9rem;
            min-height: 20px;
        }
        .feedback.correct { color: #059669; font-weight: 600; }
        .feedback.wrong { color: #dc2626; }
        .btn-row {
            margin-top: 24px;
            display: flex;
            gap: 12px;
        }
        .submit-btn {
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            background: #4f46e5;
            color: #fff;
            font-size: 0.95rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: background 0.15s;
        }
        .submit-btn:hover:not(:disabled) { background: #4338ca; }
        .submit-btn:disabled { background: #a5b4fc; cursor: default; }
        .next-btn {
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            background: #ecfdf5;
            color: #059669;
            font-size: 0.95rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: background 0.15s;
            display: none;
        }
        .next-btn:hover { background: #d1fae5; }
        .summary-panel {
            max-width: 680px;
            margin: 0 auto;
            background: #fff;
            border-radius: 12px;
            padding: 48px 36px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            text-align: center;
            display: none;
        }
        .summary-panel h2 {
            font-size: 1.4rem;
            font-weight: 700;
            color: #111;
            margin-bottom: 12px;
        }
        .summary-panel p {
            font-size: 1rem;
            color: #555;
            margin-bottom: 28px;
        }
        .summary-panel .errors { color: #dc2626; font-weight: 700; }
        @media (max-width: 480px) {
            .exercise-panel { padding: 24px 20px; }
            .stats-panel { padding: 14px 20px; }
        }
    </style>
</head>
<body>
    <div class="stats-panel">
        <span class="stats-text" id="statsText">0 done / <span class="errors">0 errors</span></span>
        <button class="complete-btn" onclick="history.back()">Complete</button>
    </div>
    <div class="exercise-panel" id="exercisePanel">
        <div class="exercise-type" id="exerciseType"></div>
        <div class="exercise-header" id="exerciseHeader">Loading exercises...</div>
        <input class="answer-input" id="answerInput" type="text" placeholder="Type your answer…" autocomplete="off" autocorrect="off" spellcheck="false">
        <div class="feedback" id="feedback"></div>
        <div class="btn-row">
            <button class="submit-btn" id="submitBtn">Check</button>
            <button class="next-btn" id="nextBtn">Next →</button>
        </div>
    </div>
    <div class="summary-panel" id="summaryPanel">
        <h2>All done!</h2>
        <p id="summaryText"></p>
        <button class="complete-btn" onclick="history.back()">Back</button>
    </div>
    <script>
        const params = new URLSearchParams(window.location.search);
        const topicId = params.get('id');
        const blockIndex = parseInt(params.get('block') || '0', 10);
        const blockNum = blockIndex + 1;

        let exercises = [];
        let current = 0;
        let done = 0;
        let errors = 0;

        function shuffle(arr) {
            for (let i = arr.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
            return arr;
        }

        async function loadAllExercises() {
            const all = [];
            let i = 1;
            while (true) {
                const url = `../content/vocabulary/${topicId}/block_${blockNum}_exercises_${i}.json`;
                const resp = await fetch(url);
                if (!resp.ok) break;
                const data = await resp.json();
                all.push(...(data.exercises || []));
                i++;
            }
            return shuffle(all);
        }

        function updateStats() {
            document.getElementById('statsText').innerHTML =
                `${done} done / <span class="errors">${errors} errors</span>`;
        }

        function showExercise(ex) {
            const typeLabel = { translate: 'Translate' }[ex.type] || ex.type;
            document.getElementById('exerciseType').textContent = typeLabel;
            document.getElementById('exerciseHeader').textContent = ex.header;

            const input = document.getElementById('answerInput');
            input.value = '';
            input.disabled = false;
            input.className = 'answer-input';
            input.style.display = '';

            document.getElementById('feedback').textContent = '';
            document.getElementById('feedback').className = 'feedback';
            document.getElementById('submitBtn').disabled = false;
            document.getElementById('submitBtn').style.display = '';
            document.getElementById('nextBtn').style.display = 'none';

            input.focus();
        }

        function checkAnswer(ex) {
            const input = document.getElementById('answerInput');
            const userAnswer = input.value.trim().toLowerCase();
            const correct = ex.answer.trim().toLowerCase();
            const isCorrect = userAnswer === correct;

            input.disabled = true;
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('nextBtn').style.display = '';

            done++;
            if (!isCorrect) {
                errors++;
                input.classList.add('wrong');
                document.getElementById('feedback').textContent = `Correct answer: ${ex.answer}`;
                document.getElementById('feedback').className = 'feedback wrong';
            } else {
                input.classList.add('correct');
                document.getElementById('feedback').textContent = 'Correct!';
                document.getElementById('feedback').className = 'feedback correct';
            }
            updateStats();
        }

        function advance() {
            current++;
            if (current >= exercises.length) {
                document.getElementById('exercisePanel').style.display = 'none';
                const summary = document.getElementById('summaryPanel');
                summary.style.display = 'block';
                document.getElementById('summaryText').innerHTML =
                    `${done} done${errors > 0 ? `, <span class="errors">${errors} errors</span>` : ', no errors!'}`;
                return;
            }
            showExercise(exercises[current]);
        }

        document.getElementById('submitBtn').addEventListener('click', () => {
            const input = document.getElementById('answerInput');
            if (!input.value.trim()) return;
            checkAnswer(exercises[current]);
        });

        document.getElementById('answerInput').addEventListener('keydown', e => {
            if (e.key === 'Enter') {
                const submitBtn = document.getElementById('submitBtn');
                const nextBtn = document.getElementById('nextBtn');
                if (!submitBtn.disabled && submitBtn.style.display !== 'none') {
                    const input = document.getElementById('answerInput');
                    if (input.value.trim()) checkAnswer(exercises[current]);
                } else if (nextBtn.style.display !== 'none') {
                    advance();
                }
            }
        });

        document.getElementById('nextBtn').addEventListener('click', advance);

        loadAllExercises().then(exs => {
            exercises = exs;
            if (!exercises.length) {
                document.getElementById('exerciseHeader').textContent = 'No exercises available for this block.';
                document.getElementById('answerInput').style.display = 'none';
                document.getElementById('submitBtn').style.display = 'none';
                return;
            }
            showExercise(exercises[0]);
        });
    </script>
</body>
</html>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8000/vocabulary/exercises.html?id=personal_information&block=0`

Expected:
- Stats panel shows "0 done / 0 errors"
- Exercise shown with type label "Translate" and the header text
- Typing correct answer and clicking Check: input turns green, "Correct!" shown, Next appears
- Typing wrong answer: input turns red, correct answer shown, error count increments
- Pressing Enter submits / advances (same as clicking button)
- After last exercise: exercise panel hides, summary panel shows
- Complete/Back button calls `history.back()`
- Verify exercises come from both `block_1_exercises_1.json` and `block_1_exercises_2.json` (≥4 exercises total for block 0)

- [ ] **Step 3: Commit**

```bash
git add vocabulary/exercises.html
git commit -m "feat: add vocabulary exercises page with stats and answer checking"
```

---

## Task 4: `vocabulary/read.html`

**Files:**
- Create: `vocabulary/read.html`

- [ ] **Step 1: Create the file with full implementation**

Create `vocabulary/read.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Read – Greek Tutorial</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f0;
            color: #1a1a1a;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .top-panel {
            max-width: 680px;
            margin: 0 auto 20px;
            background: #fff;
            border-radius: 12px;
            padding: 16px 28px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .listen-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 18px;
            border: none;
            border-radius: 8px;
            background: #eef2ff;
            color: #4f46e5;
            font-size: 0.9rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: background 0.15s;
        }
        .listen-btn:hover { background: #e0e7ff; }
        .listen-btn.playing { background: #ede9fe; color: #7c3aed; }
        .sentences-list {
            max-width: 680px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .sentence-row {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            overflow: hidden;
            cursor: pointer;
        }
        .sentence-text {
            padding: 18px 28px;
            font-size: 1rem;
            font-weight: 500;
            color: #1a1a1a;
            user-select: none;
        }
        .sentence-row:hover .sentence-text { background: #f8f7ff; }
        .sentence-translation {
            display: none;
            padding: 0 28px 16px;
            font-size: 0.9rem;
            color: #888;
            border-top: 1px solid #f0f0f0;
        }
        .sentence-row.open .sentence-translation { display: block; }
        @media (max-width: 480px) {
            .sentence-text { padding: 16px 20px; }
            .sentence-translation { padding: 0 20px 14px; }
            .top-panel { padding: 14px 20px; }
        }
    </style>
</head>
<body>
    <div class="top-panel">
        <button class="listen-btn" id="listenBtn">▶ Listen</button>
    </div>
    <div class="sentences-list" id="sentencesList"></div>
    <script>
        const params = new URLSearchParams(window.location.search);
        const topicId = params.get('id');
        const blockIndex = parseInt(params.get('block') || '0', 10);
        const blockNum = blockIndex + 1;

        const audio = new Audio(`../content/vocabulary/${topicId}/story_block_${blockNum}.mp3`);
        const listenBtn = document.getElementById('listenBtn');

        listenBtn.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
                listenBtn.textContent = '⏸ Pause';
                listenBtn.classList.add('playing');
            } else {
                audio.pause();
                listenBtn.textContent = '▶ Listen';
                listenBtn.classList.remove('playing');
            }
        });

        audio.addEventListener('ended', () => {
            listenBtn.textContent = '▶ Listen';
            listenBtn.classList.remove('playing');
        });

        fetch(`../content/vocabulary/${topicId}/vocabulary.json`)
            .then(r => { if (!r.ok) throw new Error(); return r.json(); })
            .then(data => {
                const block = (data.blocks || [])[blockIndex];
                if (!block) return;
                document.title = `Read – Block ${blockNum} – Greek Tutorial`;

                const list = document.getElementById('sentencesList');
                const sentences = (block.story && block.story.sentences) || [];

                if (!sentences.length) {
                    list.innerHTML = '<div class="sentence-row"><div class="sentence-text">No story available.</div></div>';
                    return;
                }

                sentences.forEach(s => {
                    const row = document.createElement('div');
                    row.className = 'sentence-row';
                    row.innerHTML = `
                        <div class="sentence-text">${s.sentence}</div>
                        <div class="sentence-translation">${s.translation}</div>`;
                    row.addEventListener('click', () => row.classList.toggle('open'));
                    list.appendChild(row);
                });
            });
    </script>
</body>
</html>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8000/vocabulary/read.html?id=personal_information&block=0`

Expected:
- Top panel shows "▶ Listen" button
- Sentences list shows Greek sentences
- Clicking a sentence toggles the English translation below it
- Clicking Listen plays the mp3; button changes to "⏸ Pause"
- Clicking Pause pauses playback; button reverts to "▶ Listen"
- When audio ends naturally, button reverts to "▶ Listen"

- [ ] **Step 3: Commit**

```bash
git add vocabulary/read.html
git commit -m "feat: add vocabulary read page with audio and click-to-reveal translations"
```

---

## Task 5: End-to-End Flow Verification

- [ ] **Step 1: Verify full navigation flow**

1. Open `http://localhost:8000/vocabulary/vocabulary.html`
2. Click a topic → lands on `topic.html?id=personal_information`
3. Click "Block 1. 2 items" → lands on `block.html?id=personal_information&block=0`
4. Expand items, verify details
5. Click Exercises → lands on `exercises.html?id=personal_information&block=0`, complete exercises
6. Click Complete → returns to block.html
7. Click Read → lands on `read.html?id=personal_information&block=0`
8. Click sentences and Listen button

Expected: Full flow works without broken links or JS errors in console.

- [ ] **Step 2: Verify block=1 (second block)**

Open `http://localhost:8000/vocabulary/topic.html?id=personal_information`, click "Block 2. 2 items"

Expected: block.html loads with block 2 items, exercises load from `block_2_exercises_*.json`, read page loads block 2 story.
