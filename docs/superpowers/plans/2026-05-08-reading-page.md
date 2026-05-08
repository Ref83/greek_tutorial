# Reading Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `reading/reading.html` that lists reading items from `content/reading/items.json`, and enable the Reading card on the index page.

**Architecture:** Two files change — a new `reading/reading.html` modelled exactly on `vocabulary/vocabulary.html` (fetch JSON → render cards with level badges), and `index.html` where the disabled Reading card becomes an active link. No new dependencies.

**Tech Stack:** Vanilla HTML/CSS/JS, Python HTTP server (`npm start`)

---

### Task 1: Create reading/reading.html

**Files:**
- Create: `reading/reading.html`

- [ ] **Step 1: Create the file**

Create `reading/reading.html` with the following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reading – Greek Tutorial</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

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
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }

        h1 {
            font-size: 1.6rem;
            font-weight: 600;
            color: #333;
            letter-spacing: 0.02em;
        }

        .items-list {
            max-width: 680px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .item-card {
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
            cursor: pointer;
        }

        .item-card:hover {
            box-shadow: 0 4px 16px rgba(79,70,229,0.13);
            transform: translateY(-2px);
        }

        .item-card-static {
            cursor: default;
        }

        .item-card-static:hover {
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            transform: none;
        }

        .item-name {
            font-size: 1rem;
            font-weight: 500;
            flex: 1;
            text-align: left;
        }

        .item-level {
            font-size: 0.75rem;
            font-weight: 600;
            color: #4f46e5;
            background: #ede9fe;
            border-radius: 6px;
            padding: 2px 10px;
            letter-spacing: 0.04em;
            flex-shrink: 0;
            margin-right: 16px;
            text-transform: uppercase;
        }

        .item-arrow {
            color: #4f46e5;
            font-size: 1.1rem;
        }

        @media (max-width: 480px) {
            h1 {
                font-size: 1.3rem;
            }

            .item-card {
                padding: 18px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="page-header">
        <h1>Reading</h1>
    </div>

    <div class="items-list" id="itemsList">
        <div class="item-card item-card-static">
            <span class="item-name">Loading items...</span>
        </div>
    </div>

    <script>
        const itemsList = document.getElementById('itemsList');

        fetch('../content/reading/items.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Unable to load items (${response.status})`);
                }
                return response.json();
            })
            .then(data => {
                const items = Array.isArray(data.items) ? data.items : [];
                renderItems(items);
            })
            .catch(() => {
                renderMessage('Unable to load reading items.');
            });

        function renderItems(items) {
            if (!items.length) {
                renderMessage('No reading items available yet.');
                return;
            }

            itemsList.textContent = '';

            items.forEach(item => {
                const link = document.createElement('a');
                link.className = 'item-card';
                link.href = `item.html?id=${encodeURIComponent(item.id)}`;
                link.innerHTML = `
                    <span class="item-level">${item.level}</span>
                    <span class="item-name">${item.caption}</span>
                    <span class="item-arrow">→</span>
                `;
                itemsList.appendChild(link);
            });
        }

        function renderMessage(message) {
            itemsList.innerHTML = '';

            const card = document.createElement('div');
            card.className = 'item-card item-card-static';

            const text = document.createElement('span');
            text.className = 'item-name';
            text.textContent = message;

            card.appendChild(text);
            itemsList.appendChild(card);
        }
    </script>
</body>
</html>
```

- [ ] **Step 2: Verify file exists**

Run: `ls reading/reading.html`
Expected: file listed without error.

- [ ] **Step 3: Start dev server and verify page loads**

Run: `npm start` then open `http://localhost:3000/reading/reading.html`
Expected: "Reading" heading, one card "Personal information" with "A1" level badge and arrow.

- [ ] **Step 4: Commit**

```bash
git add reading/reading.html
git commit -m "feat: add reading list page"
```

---

### Task 2: Enable Reading card on index.html

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Replace the disabled Reading card with an active link**

In `index.html`, replace:

```html
        <div class="section-card disabled">
            <span class="section-icon">📚</span>
            <span class="section-title">Reading</span>
            <span class="section-badge">Coming Soon</span>
        </div>
```

With:

```html
        <a class="section-card" href="reading/reading.html">
            <span class="section-icon">📚</span>
            <span class="section-title">Reading</span>
        </a>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:3000/index.html`
Expected: Reading card is no longer greyed out, hovering shows the indigo shadow, clicking navigates to `reading/reading.html`.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: enable reading section on home page"
```
